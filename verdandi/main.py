import argparse
import sys
from typing import List, Optional, Type

from verdandi.loader import BenchmarkLoader
from verdandi.runner import BenchmarkRunner


class BenchmarkProgram:
    def __init__(
        self,
        argv: Optional[List[str]] = None,
        bench_loader: Type[BenchmarkLoader] = BenchmarkLoader,
        bench_runner: Type[BenchmarkRunner] = BenchmarkRunner,
    ):
        if argv is None:
            argv = sys.argv

        self.bench_loader = bench_loader
        self.bench_runner = bench_runner

        self.parse_args(argv)
        self.run_benchmarks()

    def parse_args(self, argv: List[str]) -> None:
        parser = self._get_arg_parser()

        parser.parse_args(argv[1:], self)

        self._do_discovery()

    def _get_arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-s", "--start-directory", dest="start_dir", help="Directory to start the discovery at (defaults to '.')"
        )
        parser.add_argument(
            "-p", "--pattern", dest="pattern", help="Filename pattern used in discovery (defaults to 'bench*.py')"
        )

        return parser

    def _do_discovery(self) -> None:
        self.start_dir = "."
        self.pattern = "bench*.py"

        self.bench_loader().discover(start_dir=self.start_dir, pattern=self.pattern)

    def run_benchmarks(self) -> None:
        # bench_runner = self.bench_runner()
        pass


main = BenchmarkProgram
