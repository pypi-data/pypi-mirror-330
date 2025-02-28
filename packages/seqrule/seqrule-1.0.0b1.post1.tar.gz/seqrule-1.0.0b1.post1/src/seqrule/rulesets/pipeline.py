"""
Software Release Pipeline Rules.

This module implements sequence rules for CI/CD pipelines, with support for:
- Stage sequencing and dependencies
- Approval requirements
- Duration constraints
- Retry limits
- Required security checks
- Environment promotion rules
- Resource constraints
- Parallel execution
- Stage dependencies

Example pipeline:
    lint -> unit_tests -> security_scan -> build -> staging -> integration_tests -> prod

Each stage has properties like duration, required approvals, status, and resource requirements.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set

from ..core import AbstractObject, Sequence
from ..dsl import DSLRule


class StageStatus(Enum):
    """Status of a pipeline stage."""

    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"  # Blocked by approval or dependency
    WAITING = "waiting"  # Waiting for resources or parallel stages


class Environment(Enum):
    """Deployment environment."""

    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


class ResourceType(Enum):
    """Types of resources required by pipeline stages."""

    CPU = "cpu"  # CPU cores
    MEMORY = "memory"  # Memory in GB
    GPU = "gpu"  # GPU units
    WORKER = "worker"  # CI/CD workers
    DEPLOY_SLOT = "deploy_slot"  # Deployment slots


class PipelineStage(AbstractObject):
    """A stage in the software release pipeline."""

    def __init__(
        self,
        name: str,
        duration_mins: int,
        required_approvals: int = 0,
        environment: Optional[Environment] = None,
        retry_count: int = 0,
        status: StageStatus = StageStatus.PENDING,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        dependencies: Optional[Set[str]] = None,
        parallel_group: Optional[str] = None,
        resources: Optional[Dict[ResourceType, float]] = None,
    ):
        """
        Initialize a pipeline stage.

        Args:
            name: Stage name (e.g., "unit_tests", "deploy")
            duration_mins: Expected duration in minutes (must be positive)
            required_approvals: Number of approvals needed
            environment: Target environment for deployment stages
            retry_count: Number of times this stage has been retried
            status: Current stage status
            started_at: When the stage started
            completed_at: When the stage completed
            dependencies: Set of stage names that must complete before this stage
            parallel_group: Group name for stages that can run in parallel
            resources: Resource requirements {ResourceType: amount}
        """
        if duration_mins <= 0:
            raise ValueError("Duration must be positive")

        if retry_count < 0:
            raise ValueError("Retry count cannot be negative")

        if required_approvals < 0:
            raise ValueError("Required approvals cannot be negative")

        super().__init__(
            name=name,
            duration_mins=duration_mins,
            required_approvals=required_approvals,
            environment=environment.value if environment else None,
            retry_count=retry_count,
            status=status.value,
            started_at=started_at,
            completed_at=completed_at,
            dependencies=frozenset(dependencies) if dependencies else frozenset(),
            parallel_group=parallel_group,
            resources=resources or {},
        )

    def __repr__(self) -> str:
        return (
            f"PipelineStage(name={self['name']}, "
            f"status={self['status'].upper()}, "
            f"env={self['environment']})"
        )


def create_stage_order_rule(before: str, after: str) -> DSLRule:
    """
    Creates a rule requiring one stage to complete before another starts.

    Example:
        tests_before_deploy = create_stage_order_rule("unit_tests", "deploy")
    """

    def check_order(seq: Sequence) -> bool:
        before_passed = False
        for stage in seq:
            if stage["name"] == before:
                before_passed = stage["status"] == StageStatus.PASSED.value
            elif stage["name"] == after and not before_passed:
                return False
        return True

    return DSLRule(check_order, f"'{before}' must pass before '{after}' starts")


def create_approval_rule(stage_name: str, min_approvals: int) -> DSLRule:
    """
    Creates a rule requiring a minimum number of approvals for a stage.

    Example:
        prod_approval = create_approval_rule("prod_deploy", min_approvals=2)
    """

    def check_approvals(seq: Sequence) -> bool:
        for stage in seq:
            if (
                stage["name"] == stage_name
                and stage["required_approvals"] >= min_approvals
                and stage["status"] != StageStatus.BLOCKED.value
            ):
                return False
        return True

    return DSLRule(
        check_approvals, f"'{stage_name}' requires {min_approvals} approvals"
    )


def create_duration_rule(max_minutes: int) -> DSLRule:
    """
    Creates a rule limiting the total pipeline duration.
    Skipped and pending stages are excluded from the total duration.

    Example:
        time_limit = create_duration_rule(max_minutes=60)
    """

    def check_duration(seq: Sequence) -> bool:
        excluded_statuses = {StageStatus.SKIPPED.value, StageStatus.PENDING.value}
        total = sum(
            stage["duration_mins"]
            for stage in seq
            if stage["status"] not in excluded_statuses
        )
        return total <= max_minutes

    return DSLRule(
        check_duration, f"pipeline must complete within {max_minutes} minutes"
    )


def create_retry_rule(max_retries: int) -> DSLRule:
    """
    Creates a rule limiting the number of retries for failed stages.

    Example:
        retry_limit = create_retry_rule(max_retries=3)
    """

    def check_retries(seq: Sequence) -> bool:
        return all(stage["retry_count"] <= max_retries for stage in seq)

    return DSLRule(check_retries, f"stages can be retried at most {max_retries} times")


def create_required_stages_rule(required: Set[str]) -> DSLRule:
    """
    Creates a rule requiring certain stages to be present and passed.

    Example:
        security = create_required_stages_rule({"security_scan", "dependency_check"})
    """

    def check_required(seq: Sequence) -> bool:
        completed = {
            stage["name"]
            for stage in seq
            if stage["status"] == StageStatus.PASSED.value
        }
        return required.issubset(completed)

    return DSLRule(check_required, f"stages {required} must pass")


def create_environment_promotion_rule() -> DSLRule:
    """
    Creates a rule enforcing proper environment promotion order.

    Example:
        promotion = create_environment_promotion_rule()  # dev -> staging -> prod
    """
    env_order = {
        Environment.DEV.value: 0,
        Environment.STAGING.value: 1,
        Environment.PROD.value: 2,
    }

    def check_promotion(seq: Sequence) -> bool:
        last_env_level = -1
        for stage in seq:
            if stage["environment"] is not None:
                current_level = env_order[stage["environment"]]
                if current_level < last_env_level:
                    return False
                last_env_level = current_level
        return True

    return DSLRule(check_promotion, "environments must be promoted in order")


def create_dependency_rule() -> DSLRule:
    """
    Creates a rule ensuring all stage dependencies are satisfied.

    Example:
        dependencies = create_dependency_rule()
    """

    def check_dependencies(seq: Sequence) -> bool:
        completed_stages = {
            stage["name"]
            for stage in seq
            if stage["status"] == StageStatus.PASSED.value
        }

        for stage in seq:
            if stage["status"] not in {
                StageStatus.PENDING.value,
                StageStatus.BLOCKED.value,
                StageStatus.SKIPPED.value,
            }:
                # Check if all dependencies are completed
                if not stage["dependencies"].issubset(completed_stages):
                    return False
        return True

    return DSLRule(check_dependencies, "all stage dependencies must be satisfied")


def create_resource_limit_rule(resource_type: ResourceType, limit: float) -> DSLRule:
    """
    Creates a rule limiting total resource usage across parallel stages.

    Example:
        cpu_limit = create_resource_limit_rule(ResourceType.CPU, limit=8)
    """

    def check_resources(seq: Sequence) -> bool:
        # Group stages by parallel group
        parallel_groups: Dict[Optional[str], List[AbstractObject]] = {}
        for stage in seq:
            if stage["status"] == StageStatus.RUNNING.value:
                group = stage["parallel_group"]
                if group not in parallel_groups:
                    parallel_groups[group] = []
                parallel_groups[group].append(stage)

        # Check resource usage in each group
        for stages in parallel_groups.values():
            total = sum(stage["resources"].get(resource_type, 0) for stage in stages)
            if total > limit:
                return False
        return True

    return DSLRule(
        check_resources, f"total {resource_type.value} usage must not exceed {limit}"
    )


# Common pipeline rules
tests_before_deploy = create_stage_order_rule("unit_tests", "deploy")
staging_before_prod = create_stage_order_rule("staging_deploy", "prod_deploy")
security_requirements = create_required_stages_rule(
    {"security_scan", "dependency_check"}
)
prod_approval_rule = create_approval_rule("prod_deploy", min_approvals=2)
pipeline_duration = create_duration_rule(max_minutes=100)
retry_limit = create_retry_rule(max_retries=3)
environment_promotion = create_environment_promotion_rule()
dependency_check = create_dependency_rule()
cpu_limit = create_resource_limit_rule(ResourceType.CPU, limit=8)
memory_limit = create_resource_limit_rule(ResourceType.MEMORY, limit=32)

# Example pipeline configuration with parallel stages and dependencies
example_pipeline = [
    PipelineStage(
        "lint",
        duration_mins=5,
        parallel_group="static_analysis",
        resources={ResourceType.CPU: 1, ResourceType.MEMORY: 2},
    ),
    PipelineStage(
        "type_check",
        duration_mins=5,
        parallel_group="static_analysis",
        resources={ResourceType.CPU: 1, ResourceType.MEMORY: 2},
    ),
    PipelineStage(
        "unit_tests",
        duration_mins=10,
        dependencies={"lint", "type_check"},
        resources={ResourceType.CPU: 4, ResourceType.MEMORY: 8},
    ),
    PipelineStage(
        "security_scan",
        duration_mins=15,
        parallel_group="security",
        resources={ResourceType.CPU: 2, ResourceType.MEMORY: 4},
    ),
    PipelineStage(
        "dependency_check",
        duration_mins=5,
        parallel_group="security",
        resources={ResourceType.CPU: 1, ResourceType.MEMORY: 2},
    ),
    PipelineStage(
        "build",
        duration_mins=8,
        dependencies={"unit_tests", "security_scan", "dependency_check"},
        resources={ResourceType.CPU: 4, ResourceType.MEMORY: 16},
    ),
    PipelineStage(
        "staging_deploy",
        duration_mins=10,
        required_approvals=1,
        environment=Environment.STAGING,
        dependencies={"build"},
        resources={ResourceType.DEPLOY_SLOT: 1},
    ),
    PipelineStage(
        "integration_tests",
        duration_mins=20,
        dependencies={"staging_deploy"},
        resources={ResourceType.CPU: 2, ResourceType.MEMORY: 4},
    ),
    PipelineStage(
        "prod_deploy",
        duration_mins=15,
        required_approvals=2,
        environment=Environment.PROD,
        dependencies={"integration_tests"},
        resources={ResourceType.DEPLOY_SLOT: 1},
    ),
]
