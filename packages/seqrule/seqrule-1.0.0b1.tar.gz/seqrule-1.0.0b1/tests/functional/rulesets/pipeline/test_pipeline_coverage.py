import unittest
from datetime import datetime

from seqrule.rulesets.pipeline import (
    Environment,
    PipelineStage,
    ResourceType,
    StageStatus,
    create_approval_rule,
    create_dependency_rule,
    create_duration_rule,
    create_environment_promotion_rule,
    create_required_stages_rule,
    create_resource_limit_rule,
    create_retry_rule,
    create_stage_order_rule,
)


class TestPipelineCoverage(unittest.TestCase):
    """Test cases for pipeline.py to improve coverage."""

    def test_pipeline_stage_constructor_validation(self):
        """Test PipelineStage constructor validation for various parameters."""
        # Test with valid parameters
        stage = PipelineStage(
            name="Build",
            duration_mins=30,
            required_approvals=2,
            environment=Environment.DEV,
            retry_count=3,
        )
        self.assertEqual(stage["name"], "Build")
        self.assertEqual(stage["duration_mins"], 30)
        self.assertEqual(stage["required_approvals"], 2)
        self.assertEqual(stage["environment"], "dev")
        self.assertEqual(stage["retry_count"], 3)

        # Test with invalid duration_mins
        with self.assertRaises(ValueError):
            PipelineStage(
                name="Build",
                duration_mins=-10,  # Invalid: negative duration
                environment=Environment.DEV,
            )

        # Test with invalid required_approvals
        with self.assertRaises(ValueError):
            PipelineStage(
                name="Build",
                duration_mins=30,
                required_approvals=-1,  # Invalid: negative approvals
                environment=Environment.DEV,
            )

        # Test with invalid retry_count
        with self.assertRaises(ValueError):
            PipelineStage(
                name="Build",
                duration_mins=30,
                environment=Environment.DEV,
                retry_count=-2,  # Invalid: negative retry count
            )

    def test_pipeline_stage_repr(self):
        """Test the __repr__ method of PipelineStage."""
        # Create a stage with specific attributes
        stage = PipelineStage(
            name="Build",
            duration_mins=30,
            required_approvals=2,
            environment=Environment.DEV,
            retry_count=3,
            status=StageStatus.RUNNING,
            started_at=datetime(2023, 1, 1, 12, 0, 0),
            completed_at=datetime(2023, 1, 1, 12, 30, 0),
        )

        # Check that the __repr__ method returns the expected string
        repr_str = repr(stage)
        self.assertIn("Build", repr_str)
        self.assertIn("RUNNING", repr_str)
        self.assertIn("dev", repr_str)  # Environment.DEV.value is "dev"

    def test_stage_order_rule(self):
        """Test create_stage_order_rule with various inputs."""
        # Create stages with dependencies
        build = PipelineStage(
            name="Build", duration_mins=30, environment=Environment.DEV
        )
        test = PipelineStage(
            name="Test",
            duration_mins=60,
            environment=Environment.DEV,
            dependencies=["Build"],
        )
        deploy = PipelineStage(
            name="Deploy",
            duration_mins=90,
            environment=Environment.PROD,
            dependencies=["Test"],
        )

        # Set the status of build to PASSED to satisfy the rule
        build_passed = PipelineStage(
            name="Build",
            duration_mins=30,
            environment=Environment.DEV,
            status=StageStatus.PASSED,
        )

        # Create a rule that checks stage order
        rule = create_stage_order_rule("Build", "Test")

        # Create a sequence with stages in the correct order and build has passed
        seq = [build_passed, test, deploy]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence where build has not passed
        seq = [build, test, deploy]  # Build is not PASSED

        # Check that the sequence violates the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_approval_rule(self):
        """Test create_approval_rule with various inputs."""
        # Create stages with different required approvals
        dev_stage = PipelineStage(
            name="Dev",
            duration_mins=30,
            environment=Environment.DEV,
            required_approvals=0,
        )
        test_stage = PipelineStage(
            name="Test",
            duration_mins=60,
            environment=Environment.DEV,
            required_approvals=1,
        )
        prod_stage = PipelineStage(
            name="Prod",
            duration_mins=90,
            environment=Environment.PROD,
            required_approvals=2,
        )

        # Create a blocked prod stage
        blocked_prod = PipelineStage(
            name="Prod",
            duration_mins=90,
            environment=Environment.PROD,
            required_approvals=2,
            status=StageStatus.BLOCKED,
        )

        # Create a rule that checks approval requirements
        rule = create_approval_rule("Prod", 2)

        # Create a sequence with a blocked prod stage (should pass the rule)
        seq = [dev_stage, test_stage, blocked_prod]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with a non-blocked prod stage (should fail the rule)
        seq = [dev_stage, test_stage, prod_stage]

        # Check that the sequence violates the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_environment_promotion_rule(self):
        """Test create_environment_promotion_rule with various inputs."""
        # Create stages with different environments
        dev_stage = PipelineStage(
            name="Dev", duration_mins=30, environment=Environment.DEV
        )
        staging_stage = PipelineStage(
            name="Staging", duration_mins=60, environment=Environment.STAGING
        )
        prod_stage = PipelineStage(
            name="Prod", duration_mins=90, environment=Environment.PROD
        )

        # Create a rule that checks environment transitions
        rule = create_environment_promotion_rule()

        # Create a sequence with valid environment transitions
        seq = [dev_stage, staging_stage, prod_stage]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with invalid environment transitions
        seq = [dev_stage, prod_stage, staging_stage]  # PROD should come after STAGING

        # Check that the sequence violates the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_resource_limit_rule(self):
        """Test create_resource_limit_rule with various inputs."""
        # Create stages with different resource requirements
        stage1 = PipelineStage(
            name="Stage1",
            duration_mins=30,
            environment=Environment.DEV,
            resources={ResourceType.CPU: 2, ResourceType.MEMORY: 4},
            status=StageStatus.RUNNING,
        )
        stage2 = PipelineStage(
            name="Stage2",
            duration_mins=60,
            environment=Environment.DEV,
            resources={ResourceType.CPU: 4, ResourceType.MEMORY: 8},
            status=StageStatus.RUNNING,
        )

        # Create a rule that checks resource constraints for CPU
        rule = create_resource_limit_rule(ResourceType.CPU, 6)

        # Create a sequence with stages that fit within the CPU limit
        seq = [stage1, stage2]  # Total CPU: 2 + 4 = 6

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a stage with higher CPU usage
        stage3 = PipelineStage(
            name="Stage3",
            duration_mins=90,
            environment=Environment.DEV,
            resources={ResourceType.CPU: 1, ResourceType.MEMORY: 2},
            status=StageStatus.RUNNING,
        )

        # Create a sequence that exceeds the CPU limit
        seq = [stage1, stage2, stage3]  # Total CPU: 2 + 4 + 1 = 7

        # Check that the sequence violates the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_dependency_rule(self):
        """Test create_dependency_rule with various inputs."""
        # Create stages with dependencies
        build = PipelineStage(
            name="Build",
            duration_mins=30,
            environment=Environment.DEV,
            status=StageStatus.PASSED,
        )
        test = PipelineStage(
            name="Test",
            duration_mins=60,
            environment=Environment.DEV,
            dependencies=["Build"],
            status=StageStatus.RUNNING,
        )
        deploy = PipelineStage(
            name="Deploy",
            duration_mins=90,
            environment=Environment.PROD,
            dependencies=["Test"],
            status=StageStatus.PENDING,
        )

        # Create a rule that checks dependencies
        rule = create_dependency_rule()

        # Create a sequence with stages that satisfy dependencies
        seq = [build, test, deploy]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with a missing dependency
        missing_build = PipelineStage(
            name="BuildX",
            duration_mins=30,
            environment=Environment.DEV,
            status=StageStatus.PASSED,
        )
        test_with_missing_dep = PipelineStage(
            name="Test",
            duration_mins=60,
            environment=Environment.DEV,
            dependencies=["Build"],  # Depends on "Build" but we have "BuildX"
            status=StageStatus.RUNNING,
        )
        seq = [missing_build, test_with_missing_dep, deploy]

        # Check that the sequence violates the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_duration_rule(self):
        """Test create_duration_rule with various inputs."""
        # Create stages with different durations and statuses
        stage1 = PipelineStage(
            name="Stage1",
            duration_mins=30,
            environment=Environment.DEV,
            status=StageStatus.RUNNING,
        )
        stage2 = PipelineStage(
            name="Stage2",
            duration_mins=60,
            environment=Environment.DEV,
            status=StageStatus.RUNNING,
        )
        stage3 = PipelineStage(
            name="Stage3",
            duration_mins=90,
            environment=Environment.DEV,
            status=StageStatus.RUNNING,
        )

        # Create a rule that checks total duration
        rule = create_duration_rule(180)  # Max 180 minutes

        # Create a sequence with stages that fit within the duration limit
        seq = [stage1, stage2, stage3]  # Total: 30 + 60 + 90 = 180 minutes

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a stage with additional duration
        stage4 = PipelineStage(
            name="Stage4",
            duration_mins=10,
            environment=Environment.DEV,
            status=StageStatus.RUNNING,
        )

        # Create a sequence that exceeds the duration limit
        seq = [stage1, stage2, stage3, stage4]  # Total: 30 + 60 + 90 + 10 = 190 minutes

        # Check that the sequence violates the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_required_stages_rule(self):
        """Test create_required_stages_rule with various inputs."""
        # Create stages with PASSED status
        build = PipelineStage(
            name="Build",
            duration_mins=30,
            environment=Environment.DEV,
            status=StageStatus.PASSED,
        )
        test = PipelineStage(
            name="Test",
            duration_mins=60,
            environment=Environment.DEV,
            status=StageStatus.PASSED,
        )
        deploy = PipelineStage(
            name="Deploy",
            duration_mins=90,
            environment=Environment.PROD,
            status=StageStatus.RUNNING,
        )

        # Create a rule that checks for required stages
        rule = create_required_stages_rule({"Build", "Test"})

        # Create a sequence with all required stages passed
        seq = [build, test, deploy]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a sequence with a required stage not passed
        not_passed_test = PipelineStage(
            name="Test",
            duration_mins=60,
            environment=Environment.DEV,
            status=StageStatus.RUNNING,  # Not PASSED
        )
        seq = [build, not_passed_test, deploy]

        # Check that the sequence violates the rule
        result = rule(seq)
        self.assertFalse(result)

    def test_retry_rule(self):
        """Test create_retry_rule with various inputs."""
        # Create stages with different retry counts
        stage1 = PipelineStage(
            name="Stage1", duration_mins=30, environment=Environment.DEV, retry_count=2
        )
        stage2 = PipelineStage(
            name="Stage2", duration_mins=60, environment=Environment.DEV, retry_count=3
        )

        # Create a rule that checks retry limits
        rule = create_retry_rule(3)  # Max 3 retries

        # Create a sequence with stages that are within retry limits
        seq = [stage1, stage2]

        # Check that the sequence satisfies the rule
        result = rule(seq)
        self.assertTrue(result)

        # Create a stage that exceeds retry limits
        stage3 = PipelineStage(
            name="Stage3", duration_mins=90, environment=Environment.DEV, retry_count=4
        )

        # Create a sequence with a stage that exceeds retry limits
        seq = [stage1, stage2, stage3]  # stage3 has 4 retries, exceeding limit of 3

        # Check that the sequence violates the rule
        result = rule(seq)
        self.assertFalse(result)
