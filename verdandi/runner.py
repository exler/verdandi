import tracemalloc
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from statistics import mean
from time import perf_counter
from typing import Any, Callable, Dict, List, Type

from verdandi.benchmark import Benchmark
from verdandi.cli import print_header
from verdandi.result import BenchmarkResult, ResultType
from verdandi.utils import flatten


class BenchmarkRunner:
    result_class = BenchmarkResult

    def __init__(self, show_stdout: bool = False, show_stderr: bool = True) -> None:
        self.show_stdout = show_stdout
        self.show_stderr = show_stderr

    def run(self, benchmarks: List[Benchmark]) -> None:
        results: List[List[BenchmarkResult]] = []

        for benchmark in flatten(benchmarks):
            result = self.run_class(benchmark)
            results.append(result)

        if self.show_stdout:
            print_header("Captured stdout")
            for class_result in results:
                for method_result in class_result:
                    method_result.print_stdout()

        if self.show_stderr:
            print_header("Captured stderr")
            for class_result in results:
                for method_result in class_result:
                    method_result.print_stderr()

    def run_class(self, benchmark_class: Type[Benchmark], iterations: int = 10) -> List[BenchmarkResult]:
        benchmark = benchmark_class()
        methods = benchmark.collect_bench_methods()

        results = []

        benchmark.setUpClass()

        for method in methods:
            stats: List[Dict[str, Any]] = []
            stdouts: List[str] = []
            stderrs: List[str] = []
            exceptions: List[Exception] = []

            benchmark.setUp()

            for _ in range(iterations):
                benchmark.setUpIter()

                with redirect_stdout(StringIO()) as stdout, redirect_stderr(StringIO()) as stderr:
                    iter_stats = self.measure(method)

                stdouts.append(stdout.getvalue())
                stderrs.append(stderr.getvalue())
                stats.append(iter_stats)

                benchmark.tearDownIter()

            benchmark.tearDown()

            result = BenchmarkResult(
                name=benchmark.__class__.__name__ + "." + method.__name__,
                rtype=ResultType.OK,
                stdout=stdouts,
                stderr=stderrs,
                exceptions=exceptions,
                duration_sec=mean([s["time"] for s in stats]),
                # StatisticDiff is sorted from biggest to the smallest
                memory_diff=mean([s["memory"][0].size_diff for s in stats]),
            )
            print(str(result))
            results.append(result)

        benchmark.tearDownClass()

        return results

    def measure(self, func: Callable[..., Any]) -> Dict[str, Any]:
        tracemalloc.start()

        start_time = perf_counter()
        start_snapshot = tracemalloc.take_snapshot()

        func()

        stop_snapshot = tracemalloc.take_snapshot()
        stop_time = perf_counter()

        time_taken = stop_time - start_time
        memory_diff = stop_snapshot.compare_to(start_snapshot, "lineno")

        tracemalloc.stop()

        stats = {"time": time_taken, "memory": memory_diff}

        return stats
