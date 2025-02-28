#!/usr/bin/env python3
"""
Rule Analysis Script

This script provides comprehensive analysis of rule generators in the general.py module,
including complexity analysis, performance benchmarking, and optimization suggestions.

Features:
- Complexity analysis (time/space)
- Performance benchmarking with different sequence sizes
- Memory usage profiling
- Test coverage analysis
- Visualization of performance trends
- Real-world usage examples
- Optimization suggestions
- Rule scoring and complexity levels
"""

import inspect
import json
import time
import timeit
import statistics
from typing import Any, Dict, List, Callable, Set, Optional, Tuple, Union
from dataclasses import dataclass, field
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor, as_completed

from seqrule import AbstractObject, DSLRule
from seqrule.analysis import RuleAnalyzer, RuleScorer, ComplexityScore
from seqrule.rulesets.general import create_property_match_rule
from seqrule.rulesets import general


@dataclass
class BenchmarkResult:
    """Results from performance benchmarking."""
    sequence_size: int
    avg_time: float
    std_dev: float
    peak_memory: float
    gc_collections: int


@dataclass
class RuleAnalysisResult:
    """Complete analysis results for a rule generator."""
    name: str
    signature: str
    description: str
    complexity_analysis: Dict[str, Any]
    benchmarks: List[BenchmarkResult]
    test_coverage: float
    properties_accessed: Dict[str, Dict[str, Any]]
    optimization_suggestions: List[str]
    example_usage: str
    error: Optional[str] = None
    scores: Dict[str, Any] = field(default_factory=dict)
    size_time_correlation: Optional[float] = None


def create_diverse_sequences(sizes: List[int]) -> Dict[int, List[List[AbstractObject]]]:
    """Create diverse test sequences of different sizes."""
    sequences = {}
    for size in sizes:
        sequences[size] = [
            # Card-like sequence
            [
                AbstractObject(
                    value=i,
                    suit=["hearts", "diamonds", "clubs", "spades"][i % 4],
                    color="red" if i % 4 < 2 else "black",
                    rank=["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"][i % 13],
                    is_face_card=i % 13 > 9,
                    numeric_value=(i % 13) + 1,
                    property_name="suit",
                    property_value=["hearts", "diamonds", "clubs", "spades"][i % 4],
                    group=["face", "number", "ace"][0 if i % 13 > 9 else (2 if i % 13 == 0 else 1)],
                    pattern=["red-black", "high-low", "same-suit"][i % 3],
                    trend=i,
                    ratio=i / (size or 1),
                    stat=i * 1.5,
                    properties={
                        "suit": ["hearts", "diamonds", "clubs", "spades"][i % 4],
                        "color": "red" if i % 4 < 2 else "black",
                        "rank": ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"][i % 13],
                        "is_face_card": i % 13 > 9,
                        "numeric_value": (i % 13) + 1
                    }
                ) for i in range(size)
            ],
            # DNA-like sequence
            [
                AbstractObject(
                    value=i,
                    base=["A", "T", "G", "C"][i % 4],
                    position=i,
                    is_gc=["A", "T", "G", "C"][i % 4] in ["G", "C"],
                    strand="forward" if i % 2 == 0 else "reverse",
                    methylated=i % 3 == 0,
                    property_name="base",
                    property_value=["A", "T", "G", "C"][i % 4],
                    group=["gc", "at"][0 if ["A", "T", "G", "C"][i % 4] in ["G", "C"] else 1],
                    pattern=["gc-rich", "at-rich", "mixed"][i % 3],
                    trend=i,
                    ratio=i / (size or 1),
                    stat=i * 1.5,
                    properties={
                        "base": ["A", "T", "G", "C"][i % 4],
                        "position": i,
                        "is_gc": ["A", "T", "G", "C"][i % 4] in ["G", "C"],
                        "strand": "forward" if i % 2 == 0 else "reverse",
                        "methylated": i % 3 == 0,
                        "pair": ["T", "A", "C", "G"][i % 4]
                    }
                ) for i in range(size)
            ],
            # Pipeline-like sequence
            [
                AbstractObject(
                    value=i,
                    stage=["build", "test", "deploy", "validate"][i % 4],
                    status=["pending", "running", "completed", "failed"][i % 4],
                    duration=i * 10,
                    environment=["dev", "staging", "prod"][i % 3],
                    retries=i % 3,
                    resources={"cpu": i % 4 + 1, "memory": (i % 4 + 1) * 1024},
                    property_name="stage",
                    property_value=["build", "test", "deploy", "validate"][i % 4],
                    group=["dev", "prod"][i % 2],
                    pattern=["sequential", "parallel", "conditional"][i % 3],
                    trend=i,
                    ratio=i / (size or 1),
                    stat=i * 1.5,
                    properties={
                        "stage": ["build", "test", "deploy", "validate"][i % 4],
                        "status": ["pending", "running", "completed", "failed"][i % 4],
                        "duration": i * 10,
                        "environment": ["dev", "staging", "prod"][i % 3],
                        "retries": i % 3,
                        "resources": {"cpu": i % 4 + 1, "memory": (i % 4 + 1) * 1024}
                    }
                ) for i in range(size)
            ],
            # Music-like sequence
            [
                AbstractObject(
                    value=i,
                    note=["C", "D", "E", "F", "G", "A", "B"][i % 7],
                    octave=i % 3 + 4,
                    duration=["whole", "half", "quarter", "eighth"][i % 4],
                    velocity=i % 128,
                    is_rest=i % 8 == 0,
                    pitch=60 + (i % 12),
                    property_name="note",
                    property_value=["C", "D", "E", "F", "G", "A", "B"][i % 7],
                    group=["chord", "scale"][i % 2],
                    pattern=["ascending", "descending", "arpeggio"][i % 3],
                    trend=i,
                    ratio=i / (size or 1),
                    stat=i * 1.5,
                    properties={
                        "note": ["C", "D", "E", "F", "G", "A", "B"][i % 7],
                        "octave": i % 3 + 4,
                        "duration": ["whole", "half", "quarter", "eighth"][i % 4],
                        "velocity": i % 128,
                        "is_rest": i % 8 == 0,
                        "pitch": 60 + (i % 12),
                        "is_chord_tone": ["C", "D", "E", "F", "G", "A", "B"][i % 7] in ["C", "E", "G"]
                    }
                ) for i in range(size)
            ]
        ]
    return sequences


def create_example_rule(generator: Callable) -> Any:
    """Create an example rule based on the generator's signature."""
    sig = inspect.signature(generator)
    params = {}
    
    # Handle variadic arguments
    if any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in sig.parameters.values()):
        # For *args parameters, provide domain-specific property names
        if "card" in generator.__name__:
            return generator("suit", "rank", "color")
        elif "dna" in generator.__name__:
            return generator("base", "position", "strand")
        elif "pipeline" in generator.__name__:
            return generator("stage", "status", "environment")
        elif "music" in generator.__name__:
            return generator("note", "octave", "duration")
        else:
            return generator("value", "type", "group")
    
    for name, param in sig.parameters.items():
        if param.annotation == str:
            if name == "property_name":
                # Use domain-specific properties based on generator name
                if "card" in generator.__name__:
                    params[name] = "suit"
                elif "dna" in generator.__name__:
                    params[name] = "base"
                elif "pipeline" in generator.__name__:
                    params[name] = "stage"
                elif "music" in generator.__name__:
                    params[name] = "note"
                else:
                    params[name] = "value"
            elif name == "mode":
                params[name] = "all"
            elif name == "scope":
                params[name] = "global"
            elif name == "trend":
                params[name] = "increasing"
            else:
                params[name] = "test"
        elif param.annotation == float:
            if "ratio" in name:
                params[name] = 0.5
            elif "tolerance" in name:
                params[name] = 0.1
            elif "min" in name:
                params[name] = 0.0
            elif "max" in name:
                params[name] = 1.0
            elif name == "target":
                params[name] = 10.0
            else:
                params[name] = 1.0
        elif param.annotation == int:
            if name == "window":
                params[name] = 3
            elif name == "group_size":
                params[name] = 2
            elif "min" in name:
                params[name] = 1
            elif "max" in name:
                params[name] = 10
            elif name == "required_count":
                params[name] = 1
            else:
                params[name] = 5
        elif param.annotation == List[DSLRule]:
            # For composite and meta rules, create domain-specific subrules
            if "card" in generator.__name__:
                params[name] = [
                    create_property_match_rule("suit", "hearts"),
                    create_property_match_rule("rank", "A")
                ]
            elif "dna" in generator.__name__:
                params[name] = [
                    create_property_match_rule("base", "G"),
                    create_property_match_rule("strand", "forward")
                ]
            elif "pipeline" in generator.__name__:
                params[name] = [
                    create_property_match_rule("stage", "build"),
                    create_property_match_rule("status", "completed")
                ]
            elif "music" in generator.__name__:
                params[name] = [
                    create_property_match_rule("note", "C"),
                    create_property_match_rule("octave", "4")
                ]
            else:
                params[name] = [
                    create_property_match_rule("value", "test"),
                    create_property_match_rule("type", "default")
                ]
        elif param.annotation == List[Any]:
            # For pattern rules, use domain-specific patterns
            if "card" in generator.__name__:
                params[name] = ["hearts", "diamonds", "clubs", "spades"]
            elif "dna" in generator.__name__:
                params[name] = ["A", "T", "G", "C"]
            elif "pipeline" in generator.__name__:
                params[name] = ["build", "test", "deploy", "validate"]
            elif "music" in generator.__name__:
                params[name] = ["C", "E", "G", "B"]
            else:
                params[name] = ["A", "B", "C", "D"]
        elif param.annotation == Dict[Any, Set[Any]]:
            # For dependency and transition rules, use domain-specific groups
            if "card" in generator.__name__:
                params[name] = {
                    "red": {"hearts", "diamonds"},
                    "black": {"clubs", "spades"},
                    "face": {"J", "Q", "K"}
                }
            elif "dna" in generator.__name__:
                params[name] = {
                    "strong": {"G", "C"},
                    "weak": {"A", "T"},
                    "methylated": {"mC", "mG"}
                }
            elif "pipeline" in generator.__name__:
                params[name] = {
                    "dev": {"build", "test"},
                    "prod": {"deploy", "validate"},
                    "failed": {"error", "timeout"}
                }
            elif "music" in generator.__name__:
                params[name] = {
                    "chord": {"C", "E", "G"},
                    "scale": {"C", "D", "E", "F", "G", "A", "B"},
                    "rest": {"quarter_rest", "half_rest"}
                }
            else:
                params[name] = {
                    "group1": {"A", "B"},
                    "group2": {"C", "D"},
                    "group3": {"E", "F"}
                }
        elif param.annotation == DSLRule:
            # For bounded sequence rules, use domain-specific rules
            if "card" in generator.__name__:
                params[name] = create_property_match_rule("suit", "hearts")
            elif "dna" in generator.__name__:
                params[name] = create_property_match_rule("base", "G")
            elif "pipeline" in generator.__name__:
                params[name] = create_property_match_rule("stage", "build")
            elif "music" in generator.__name__:
                params[name] = create_property_match_rule("note", "C")
            else:
                params[name] = create_property_match_rule("value", "test")
        elif param.annotation == Optional[Callable[[AbstractObject], bool]]:
            # For filter rules, use domain-specific predicates
            if "card" in generator.__name__:
                params[name] = lambda obj: obj.properties.get("is_face_card", False)
            elif "dna" in generator.__name__:
                params[name] = lambda obj: obj.properties.get("is_gc", False)
            elif "pipeline" in generator.__name__:
                params[name] = lambda obj: obj.properties.get("status") == "completed"
            elif "music" in generator.__name__:
                params[name] = lambda obj: not obj.properties.get("is_rest", False)
            else:
                params[name] = lambda obj: True
        elif param.annotation == Callable[[List[AbstractObject]], bool]:
            # For historical and group rules, use domain-specific group checks
            if "card" in generator.__name__:
                params[name] = lambda objs: all(obj.properties.get("color") == "red" for obj in objs)
            elif "dna" in generator.__name__:
                params[name] = lambda objs: all(obj.properties.get("is_gc", False) for obj in objs)
            elif "pipeline" in generator.__name__:
                params[name] = lambda objs: all(obj.properties.get("status") == "completed" for obj in objs)
            elif "music" in generator.__name__:
                params[name] = lambda objs: not any(obj.properties.get("is_rest", False) for obj in objs)
            else:
                params[name] = lambda objs: True
        elif param.annotation == Callable[[List[float]], float]:
            # For running stat rules, use appropriate statistical functions
            params[name] = statistics.mean
        elif param.annotation == Any:
            # For value parameter in property match rule, use domain-specific values
            if "card" in generator.__name__:
                params[name] = "hearts"
            elif "dna" in generator.__name__:
                params[name] = "G"
            elif "pipeline" in generator.__name__:
                params[name] = "build"
            elif "music" in generator.__name__:
                params[name] = "C"
            else:
                params[name] = "test"
            
    try:
        return generator(**params)
    except Exception as e:
        return f"Failed to create example rule: {str(e)}"


def benchmark_rule(rule: DSLRule, sequences: List[List[AbstractObject]], 
                  num_runs: int = 5) -> BenchmarkResult:
    """Benchmark a rule with given sequences."""
    import gc
    import tracemalloc
    
    # Time measurement with proper cleanup
    times = []
    for _ in range(num_runs):
        gc.collect()  # Clear any garbage
        start = time.perf_counter()
        for seq in sequences:
            rule(seq)
        end = time.perf_counter()
        times.append(end - start)
    
    # Memory measurement with proper cleanup
    tracemalloc.start()
    gc.collect()  # Force collection before memory measurement
    max_memory = 0
    for seq in sequences:
        rule(seq)
        current, peak = tracemalloc.get_traced_memory()
        max_memory = max(max_memory, peak)
    peak_memory = max_memory / (1024 * 1024)  # Convert to MB
    tracemalloc.stop()
    
    # GC stats
    gc.collect()
    gc_collections = sum(gc.get_count())  # Sum all generation collections
    
    return BenchmarkResult(
        sequence_size=max(len(seq) for seq in sequences),
        avg_time=statistics.mean(times),
        std_dev=statistics.stdev(times) if len(times) > 1 else 0,
        peak_memory=peak_memory,
        gc_collections=gc_collections
    )


def extract_example_usage(generator: Callable, name: str) -> str:
    """Extract example usage from docstring and test files."""
    doc = inspect.getdoc(generator) or ""
    
    # First try to get example from docstring
    example_lines = []
    in_example = False
    for line in doc.split('\n'):
        if 'Example:' in line:
            in_example = True
            continue
        if in_example:
            if line.strip() and not line.startswith('    '):
                break
            if line.strip():
                example_lines.append(line)
    
    if example_lines:
        return "From docstring:\n" + "\n".join(example_lines)
    
    # If no docstring example, look in test files
    source_file = inspect.getsourcefile(generator)
    if source_file:
        test_files = list(Path(source_file).parent.parent.glob('tests/**/test_*.py'))
        for test_file in test_files:
            with open(test_file, 'r') as f:
                test_source = f.read()
                if name in test_source:
                    # Find the test function that uses this rule
                    import ast
                    tree = ast.parse(test_source)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            func_source = test_source[node.lineno-1:node.end_lineno]
                            if name in func_source:
                                return f"From {test_file.name}:\n{func_source}"
    
    return "No example available"


def analyze_rule_generator(name: str, generator: Callable, 
                         sequences: Dict[int, List[List[AbstractObject]]],
                         analyzer: RuleAnalyzer, scorer: RuleScorer) -> RuleAnalysisResult:
    """Perform comprehensive analysis of a rule generator."""
    doc = inspect.getdoc(generator) or ""
    signature = str(inspect.signature(generator))
    
    example_rule = create_example_rule(generator)
    
    if isinstance(example_rule, str):  # Error occurred
        return RuleAnalysisResult(
            name=name,
            signature=signature,
            description=doc.split('\n')[0],
            complexity_analysis={},
            benchmarks=[],
            test_coverage=0.0,
            properties_accessed={},
            optimization_suggestions=[],
            example_usage="",
            error=example_rule,
            size_time_correlation=None
        )
    
    try:
        # Analyze the rule
        analysis = analyzer.analyze(example_rule)
        
        # Convert property access info to serializable format
        properties_info = {}
        total_accesses = 0
        for prop_name, access in analysis.properties.items():
            if isinstance(prop_name, str):  # Only include string property names
                total_accesses += access.access_count
                properties_info[prop_name] = {
                    "access_count": access.access_count,
                    "access_types": [str(t) for t in access.access_types],
                    "nested_properties": list(access.nested_properties)
                }
        
        # Get performance correlation
        size_time_correlation = None
        if analysis.performance.size_time_correlation is not None:
            size_time_correlation = float(analysis.performance.size_time_correlation)
        
        # Run benchmarks
        benchmarks = []
        for size, size_sequences in sequences.items():
            benchmark = benchmark_rule(example_rule, size_sequences)
            benchmarks.append(benchmark)
        
        # Get complexity analysis
        complexity_info = {
            "time_complexity": str(analysis.complexity.time_complexity),
            "space_complexity": str(analysis.complexity.space_complexity),
            "description": analysis.complexity.description,
            "bottlenecks": analysis.complexity.bottlenecks,
            "ast_features": analysis.complexity.ast_features,
            "total_property_accesses": total_accesses  # Add total accesses to complexity info
        }
        
        # Score the rule
        score = scorer.score(analysis)
        scores = {
            "raw_score": score.raw_score,
            "normalized_score": score.normalized_score,
            "complexity_level": str(score.complexity_level),
            "contributing_factors": score.contributing_factors,
            "recommendations": score.recommendations
        }
        
        return RuleAnalysisResult(
            name=name,
            signature=signature,
            description=doc.split('\n')[0],
            complexity_analysis=complexity_info,
            benchmarks=benchmarks,
            test_coverage=analysis.coverage,
            properties_accessed=properties_info,  # Pass the full property access info
            optimization_suggestions=analysis.optimization_suggestions,
            example_usage=extract_example_usage(generator, name),
            scores=scores,
            size_time_correlation=size_time_correlation
        )
    except Exception as e:
        import traceback
        return RuleAnalysisResult(
            name=name,
            signature=signature,
            description=doc.split('\n')[0],
            complexity_analysis={},
            benchmarks=[],
            test_coverage=0.0,
            properties_accessed={},
            optimization_suggestions=[],
            example_usage="",
            error=f"{str(e)}\n{traceback.format_exc()}",
            size_time_correlation=None
        )


def plot_performance_trends(results: List[RuleAnalysisResult], output_dir: str):
    """Generate performance visualization plots."""
    # Set style for better visualization
    sns.set_style("whitegrid")
    
    # Performance plot
    plt.figure(figsize=(15, 10))
    for result in results:
        if not result.error and result.benchmarks:
            sizes = [b.sequence_size for b in result.benchmarks]
            times = [b.avg_time for b in result.benchmarks]
            plt.plot(sizes, times, marker='o', label=result.name.replace('create_', ''))
    
    plt.xlabel('Sequence Size')
    plt.ylabel('Average Time (seconds)')
    plt.title('Rule Performance Scaling')
    plt.yscale('log')  # Use log scale for better visualization
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/performance_trends.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Memory usage plot
    plt.figure(figsize=(15, 10))
    for result in results:
        if not result.error and result.benchmarks:
            sizes = [b.sequence_size for b in result.benchmarks]
            memory = [b.peak_memory for b in result.benchmarks]
            plt.plot(sizes, memory, marker='o', label=result.name.replace('create_', ''))
    
    plt.xlabel('Sequence Size')
    plt.ylabel('Peak Memory Usage (MB)')
    plt.title('Rule Memory Usage Scaling')
    plt.yscale('log')  # Use log scale for better visualization
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/memory_trends.png", dpi=300, bbox_inches='tight')
    plt.close()


def generate_markdown_report(results: List[RuleAnalysisResult], output_dir: str) -> str:
    """Generate a comprehensive markdown report of the analysis results."""
    report = ["# Rule Analysis Report\n"]
    
    # Summary table
    summary_table = []
    headers = ["Rule", "Time Complexity", "Space Complexity", "Raw Score", "Normalized Score", "Property Accesses"]
    for result in results:
        if result.error:
            continue
        complexity = result.complexity_analysis
        raw_score = result.scores.get("raw_score", 0)
        normalized_score = result.scores.get("normalized_score", 0)
        total_accesses = sum(info["access_count"] for info in result.properties_accessed.values())
        summary_table.append([
            result.name,
            complexity["time_complexity"],
            complexity["space_complexity"],
            f"{raw_score:.2f}",
            f"{normalized_score:.1f}",
            total_accesses
        ])
    
    report.append("## Summary\n")
    report.append(tabulate(summary_table, headers=headers, tablefmt="pipe"))
    report.append("\n")
    
    # Detailed analysis for each rule
    for result in results:
        report.append(f"\n## {result.name}\n")
        
        if result.error:
            report.append(f"⚠️ Error: {result.error}\n")
            continue
        
        report.append(f"**Signature:** `{result.signature}`\n")
        report.append(f"**Description:** {result.description}\n")
        
        # Complexity Analysis
        report.append("\n### Complexity Analysis\n")
        complexity = result.complexity_analysis
        report.append(f"- Time Complexity: {complexity['time_complexity']}")
        report.append(f"- Space Complexity: {complexity['space_complexity']}")
        report.append(f"- Description: {complexity['description']}")
        if complexity['bottlenecks']:
            report.append("- Bottlenecks:")
            for bottleneck in complexity['bottlenecks']:
                report.append(f"  - {bottleneck}")
        
        # Property Access Patterns
        if result.properties_accessed:
            report.append("\n### Property Access Patterns\n")
            total_accesses = sum(info["access_count"] for info in result.properties_accessed.values())
            report.append(f"Total Property Accesses: {total_accesses}\n")
            for prop, info in result.properties_accessed.items():
                report.append(f"#### Property: `{prop}`\n")
                report.append(f"- Access Count: {info['access_count']}")
                report.append(f"- Access Types: {', '.join(info['access_types'])}")
                if info['nested_properties']:
                    report.append(f"- Nested Properties: {', '.join(info['nested_properties'])}")
            report.append("\n")
        
        # Performance Analysis
        report.append("\n### Performance Analysis\n")
        
        # Create performance table
        perf_table = []
        perf_headers = ["Sequence Size", "Avg Time (ms)", "Std Dev", "Peak Memory (MB)", "GC Collections"]
        for benchmark in result.benchmarks:
            perf_table.append([
                benchmark.sequence_size,
                f"{benchmark.avg_time * 1000:.3f}",
                f"{benchmark.std_dev * 1000:.3f}",
                f"{benchmark.peak_memory:.2f}",
                benchmark.gc_collections
            ])
        report.append(tabulate(perf_table, headers=perf_headers, tablefmt="pipe"))
        report.append("\n")
        
        # Add correlation analysis if available
        if result.size_time_correlation is not None:
            report.append(f"\nSize-Time Correlation: {result.size_time_correlation:.3f}")
            report.append("\n- Correlation interpretation:")
            if abs(result.size_time_correlation) > 0.9:
                report.append("  - Strong correlation between sequence size and execution time")
            elif abs(result.size_time_correlation) > 0.5:
                report.append("  - Moderate correlation between sequence size and execution time")
            else:
                report.append("  - Weak or no correlation between sequence size and execution time")
        
        # Scoring
        report.append("\n### Rule Scoring\n")
        scores = result.scores
        report.append(f"- Complexity Level: {scores['complexity_level']}")
        report.append(f"- Normalized Score: {scores['normalized_score']:.1f}")
        report.append("\nContributing Factors:")
        for factor, weight in scores['contributing_factors'].items():
            report.append(f"- {factor}: {weight:.1f}")
        
        # Optimization Suggestions
        if result.optimization_suggestions:
            report.append("\n### Optimization Suggestions\n")
            for suggestion in result.optimization_suggestions:
                report.append(f"- {suggestion}")
        
        # Example Usage
        report.append("\n### Example Usage\n")
        report.append("```python")
        report.append(result.example_usage)
        report.append("```\n")
    
    # Write report to file
    report_path = Path(output_dir) / "analysis_report.md"
    with open(report_path, "w") as f:
        f.write("\n".join(report))
    
    return "\n".join(report)  # Return the report content instead of the path


def get_rule_generators() -> Dict[str, Callable]:
    """Get all rule generator functions from general module."""
    return {
        name: func for name, func in inspect.getmembers(general)
        if (inspect.isfunction(func) and 
            name.startswith('create_') and 
            name.endswith('_rule'))
    }


def main():
    """Main entry point for the script."""
    print(f"SeqRule Rule Analysis")
    print(f"=====================")
    
    output_dir = Path("docs/general/built_in_rule_analyses")
    plots_dir = output_dir / "plots"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)
    
    # Create test sequences of various sizes
    sequence_sizes = [0, 1, 10, 100, 1000]
    sequences = create_diverse_sequences(sequence_sizes)
    
    # Create analyzer with all test sequences
    all_test_sequences = []
    for size in sequence_sizes:
        all_test_sequences.extend(sequences[size])
    analyzer = RuleAnalyzer().with_options(max_sequence_length=1000).with_sequences(all_test_sequences)  # Use all sequences for analysis
    
    # Create a single RuleScorer instance for all analyses
    scorer = RuleScorer()
    
    # Get and analyze all rule generators
    generators = get_rule_generators()
    results = []
    
    print(f"Analyzing {len(generators)} rule generators...")
    
    # Use ThreadPoolExecutor for parallel analysis
    with ThreadPoolExecutor() as executor:
        future_to_name = {
            executor.submit(
                analyze_rule_generator, name, generator, sequences, analyzer, scorer
            ): name
            for name, generator in generators.items()
        }
        
        for future in as_completed(future_to_name):
            name = future_to_name[future]
            try:
                result = future.result()
                results.append(result)
                print(f"✓ Analyzed {name}")
            except Exception as e:
                print(f"✗ Failed to analyze {name}: {str(e)}")
    
    # Apply batch normalization to all scores
    print("\nApplying batch normalization to scores...")
    normalized_scores = scorer.batch_normalize()
    
    # Update the scores in results
    for i, score in enumerate(normalized_scores):
        if i < len(results):
            results[i].scores = {
                "raw_score": score.raw_score,
                "normalized_score": score.normalized_score,
                "complexity_level": str(score.complexity_level),
                "contributing_factors": score.contributing_factors,
                "recommendations": score.recommendations
            }
    
    print("\nGenerating visualizations...")
    plot_performance_trends(results, plots_dir)
    
    print("Generating reports...")
    
    # Generate markdown report
    report_content = generate_markdown_report(results, output_dir)
    
    # JSON data
    def serialize_result(obj):
        if isinstance(obj, (RuleAnalysisResult, BenchmarkResult)):
            return {k: serialize_result(v) for k, v in obj.__dict__.items()}
        if isinstance(obj, ComplexityScore):
            return obj.name
        if isinstance(obj, (set, type)):
            return str(obj)
        if isinstance(obj, list):
            return [serialize_result(x) for x in obj]
        if isinstance(obj, dict):
            return {k: serialize_result(v) for k, v in obj.items()}
        # Handle RuleScore objects
        if hasattr(obj, '__dict__'):
            return {
                k: serialize_result(v) 
                for k, v in obj.__dict__.items()
                if not k.startswith('_')  # Skip private attributes
            }
        return obj

    json_file = output_dir / "rule_analysis.json"
    json_file.write_text(json.dumps([serialize_result(result) for result in results], indent=2))
    
    print(f"\nAnalysis complete! Reports generated in {output_dir}/")
    print(f"- analysis_report.md (Human readable report)")
    print(f"- rule_analysis.json (Machine readable data)")
    print("- plots/performance_trends.png (Performance visualization)")
    print("- plots/memory_trends.png (Memory usage visualization)")

    # Verify the files were created
    report_file = output_dir / "analysis_report.md"
    if not report_file.exists():
        print("\nWarning: Analysis report was not created!")
    if not json_file.exists():
        print("\nWarning: JSON file was not created!")
    if not (plots_dir / "performance_trends.png").exists():
        print("\nWarning: Performance plot was not created!")
    if not (plots_dir / "memory_trends.png").exists():
        print("\nWarning: Memory plot was not created!")


if __name__ == "__main__":
    main() 