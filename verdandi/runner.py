import sys
import tracemalloc
from collections import UserList
from io import StringIO
from statistics import mean
from time import perf_counter
from typing import Any, Callable, Dict, List

from verdandi.benchmark import Benchmark
from verdandi.result import BenchmarkResult, ResultType
from verdandi.utils import print_header


class StreamCapture(UserList):
    """
    Context manager that replaces the standard output with StringIO buffer
    and keeps the output in a list
    """

    def __enter__(self) -> None:
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args) -> None:
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


class BenchmarkRunner:
    result_class = BenchmarkResult

    def __init__(self, show_stdout: bool = False) -> None:
        self.show_stdout = show_stdout

    def run(self, benchmarks: List[Benchmark]) -> None:
        results: List[List[BenchmarkResult]] = []

        for benchmark in benchmarks:
            result = self.run_class(benchmark)
            results.append(result)

        if self.show_stdout:
            print_header("Captured stdout")
            for class_result in results:
                for method_result in class_result:
                    method_result.print_stdout()

    def run_class(self, benchmark: Benchmark, iterations: int = 10) -> None:
        benchmark = benchmark()
        methods = benchmark.collect_bench_methods()

        results: List[BenchmarkResult] = []

        tracemalloc.start()

        benchmark.setUpClass()

        for method in methods:
            stats: List[Dict[str, Any]] = []
            outputs: List[str] = []

            benchmark.setUp()

            for _ in range(iterations):
                benchmark.setUpIter()

                with StreamCapture() as output:
                    iter_stats = self.measure(method)

                outputs.append(output)
                stats.append(iter_stats)

                benchmark.tearDownIter()

            benchmark.tearDown()

            result = BenchmarkResult(
                name=benchmark.__class__.__name__ + "." + method.__name__,
                rtype=ResultType.OK,
                stdout=outputs,
                duration_sec=mean([s["time"] for s in stats]),
                # StatisticDiff is sorted from biggest to the smallest
                memory_diff=mean([s["memory"][0].size_diff for s in stats]),
            )
            result.print_result()
            results.append(result)

        benchmark.tearDownClass()

        return results

    def measure(self, func: Callable[..., Any]) -> BenchmarkResult:
        start_time = perf_counter()
        start_snapshot = tracemalloc.take_snapshot()

        func()

        stop_snapshot = tracemalloc.take_snapshot()
        stop_time = perf_counter()

        time_taken = stop_time - start_time
        memory_diff = stop_snapshot.compare_to(start_snapshot, "lineno")

        stats = {"time": time_taken, "memory": memory_diff}

        return stats
