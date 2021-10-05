import argparse
import importlib
import sys
import types
from typing import List, Optional, Type, Union

from verdandi.benchmark import Benchmark
from verdandi.loader import BenchmarkLoader
from verdandi.runner import BenchmarkRunner
from verdandi.utils import convert_name


class BenchmarkProgram:
    def __init__(
        self,
        module: Union[str, types.ModuleType] = "__main__",
        argv: Optional[List[str]] = None,
        bench_loader: Type[BenchmarkLoader] = BenchmarkLoader,
        bench_runner: Type[BenchmarkRunner] = BenchmarkRunner,
    ):
        if isinstance(module, str):
            self.module = importlib.import_module(module)
        else:
            self.module = module

        if argv is None:
            argv = sys.argv

        self.bench_loader = bench_loader()
        self.bench_runner = bench_runner()

        self.benches: List[Type[Benchmark]] = []
        self.parse_args(argv)
        self.do_discovery()
        self.run_benchmarks()

    def parse_args(self, argv: List[str]) -> None:
        parser = self._get_arg_parser()
        parser.parse_args(argv[1:], self)

    def _get_arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("benches", nargs="*", help="List of bench modules or files")
        parser.add_argument(
            "-s",
            "--start-directory",
            dest="start_dir",
            help="Directory to start the discovery at (defaults to '.')",
            default=".",
        )
        parser.add_argument(
            "-p",
            "--pattern",
            dest="pattern",
            help="Filename pattern used in discovery (defaults to 'bench*.py')",
            default="bench*.py",
        )

        return parser

    def do_discovery(self) -> None:
        if not self.benches:
            self.benches = self.bench_loader.discover(start_dir=self.start_dir, pattern=self.pattern)
        elif self.benches:
            bench_names = [convert_name(name) for name in self.benches]
            self.benches = [self.bench_loader.load_benches_from_name(name, self.module) for name in bench_names]
        else:
            self.benches = self.bench_loader.load_benches_from_module(self.module)

    def run_benchmarks(self) -> None:
        # bench_runner = self.bench_runner()
        print(self.benches)


main = BenchmarkProgram
