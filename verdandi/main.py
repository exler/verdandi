import argparse
import importlib
import os
import sys
import types
from typing import List, Optional, Type, Union

from verdandi.benchmark import Benchmark
from verdandi.loader import BenchmarkLoader
from verdandi.runner import BenchmarkRunner
from verdandi.utils import convert_name, print_header


class BenchmarkProgram:
    def __init__(
        self,
        module: Optional[Union[str, types.ModuleType]] = None,
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

        self.bench_loader = bench_loader
        self.bench_runner = bench_runner

        self.benches: List[Type[Benchmark]] = []
        self.parse_args(argv)

        print_header("Benchmark session started")
        print(f"Root directory: {os.getcwd()}")

        self.do_discovery()
        self.run_benchmarks()

    def parse_args(self, argv: List[str]) -> None:
        parser = self._get_arg_parser()
        parser.parse_args(argv[1:], self)

    def _get_arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("benches", nargs="*", help="List of bench modules or files")
        parser.add_argument(
            "-o",
            "--show-stdout",
            dest="show_stdout",
            help="Show captured stdout after benchmarks are completed",
            action="store_true",
        )
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
        loader = self.bench_loader()

        if not self.benches:
            self.benches = loader.discover(start_dir=self.start_dir, pattern=self.pattern)
        elif self.benches:
            bench_names = [convert_name(name) for name in self.benches]
            self.benches = [loader.load_benches_from_name(name) for name in bench_names]
        else:
            self.benches = loader.load_benches_from_module(self.module)

        print(f"Collected {len(self.benches)} item{'s'[:len(self.benches)^1]}")

    def run_benchmarks(self) -> None:
        runner = self.bench_runner(show_stdout=self.show_stdout)

        print()  # Use whitespace as separator here

        runner.run(self.benches)


def main(*args, **kwargs):
    """Entry point for usage in scripts"""
    BenchmarkProgram(*args, **kwargs)
