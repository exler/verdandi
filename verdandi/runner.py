from statistics import mean
from time import perf_counter
from typing import Any, Callable, List

from verdandi.benchmark import Benchmark
from verdandi.result import BenchmarkResult


class BenchmarkRunner:
    result_class = BenchmarkResult

    def measure(self, func: Callable[..., Any]) -> BenchmarkResult:
        start_time = perf_counter()

        func()

        stop_time = perf_counter()
        time_taken = stop_time - start_time
        return time_taken

    def run(self, benchmark: Benchmark, iterations: int = 10) -> None:
        benchmark = benchmark()
        methods = benchmark.collect_bench_methods()

        times: List[float] = []

        benchmark.setUpClass()

        for method in methods:
            benchmark.setUp()
            for _ in range(iterations):
                benchmark.setUpIter()

                time_taken = self.measure(method)
                times.append(time_taken)

                benchmark.tearDownIter()

            benchmark.tearDown()

        benchmark.tearDownClass()

        return BenchmarkResult(name="test", duration_sec=mean(times))
