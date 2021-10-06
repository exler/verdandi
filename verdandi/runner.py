import tracemalloc
from statistics import mean
from time import perf_counter
from typing import Any, Callable, Dict, List

from verdandi.benchmark import Benchmark
from verdandi.result import BenchmarkResult


class BenchmarkRunner:
    result_class = BenchmarkResult

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

    def run(self, benchmark: Benchmark, iterations: int = 10) -> None:
        benchmark = benchmark()
        methods = benchmark.collect_bench_methods()

        stats: List[Dict[str, Any]] = []
        tracemalloc.start()

        benchmark.setUpClass()

        for method in methods:
            benchmark.setUp()
            for _ in range(iterations):
                benchmark.setUpIter()

                iter_stats = self.measure(method)
                stats.append(iter_stats)

                benchmark.tearDownIter()

            benchmark.tearDown()

        benchmark.tearDownClass()

        return BenchmarkResult(
            name="test",
            duration_sec=mean([s["time"] for s in stats]),
            # StatisticDiff is sorted from biggest to the smallest
            memory_diff=mean([s["memory"][0].size_diff for s in stats]),
        )
