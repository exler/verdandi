import sys

from verdandi import Benchmark


class BenchmarkCapture(Benchmark):
    def bench_stdout_capture(self) -> None:
        sys.stdout.write("STDOUT")

    def bench_stderr_capture(self) -> None:
        sys.stderr.write("STDERR")

    def bench_exception_capture(self) -> None:
        raise Exception("Captured exception")
