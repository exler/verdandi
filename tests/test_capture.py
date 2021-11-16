from unittest import TestCase

from tests.benchmarks.bench_capture import BenchmarkCapture
from verdandi.result import ResultType
from verdandi.runner import BenchmarkRunner


class TestCapture(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = BenchmarkRunner()

    def test_capture(self) -> None:
        results = self.runner.run_class(BenchmarkCapture, iterations=1, print_result=False)

        for result in results:
            # TODO: Allow running single method so this test will be split into three
            if result.name == "BenchmarkCapture.bench_exception_capture":
                self.assertEqual(len(result.exceptions), 1)
                self.assertTrue(result.rtype == ResultType.ERROR)
            elif result.name == "BenchmarkCapture.bench_stderr_capture":
                self.assertTrue("STDERR" in result.stderr)
            elif result.name == "BenchmarkCapture.bench_stdout_capture":
                self.assertTrue("STDOUT" in result.stdout)
