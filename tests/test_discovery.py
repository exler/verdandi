from unittest import TestCase

from verdandi import Benchmark
from verdandi.loader import BenchmarkLoader


class TestDiscovery(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.loader = BenchmarkLoader()

    def test_file_discovery(self) -> None:
        benches = self.loader.load_benches_from_name("tests.benchmarks.bench_discovery")

        self.assertEqual(len(benches), 1)
        [self.assertTrue(issubclass(bench, Benchmark)) for bench in benches]
