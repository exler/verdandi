import argparse
import importlib
import sys
from typing import List, Optional, Type

from verdandi.loader import BenchmarkLoader
from verdandi.runner import BenchmarkRunner


class BenchmarkProgram:
    def __init__(
        self,
        module: str = "__main__",
        argv: Optional[List[str]] = None,
        bench_loader: Type[BenchmarkLoader] = BenchmarkLoader,
        bench_runner: Type[BenchmarkRunner] = BenchmarkRunner,
        catch_break: bool = False,
    ):
        if isinstance(module, str):
            self.module = importlib.import_module(module)
        else:
            self.module = module

        if argv is None:
            argv = sys.argv

        self.bench_loader = bench_loader
        self.bench_runner = bench_runner

        self.catch_break = catch_break

        self.parse_args(argv)
        self.run_benchmarks()

    def parse_args(self, argv: List[str]) -> None:
        self._init_arg_parsers()

        if self.module is None:
            if len(argv) > 1 and argv[1].lower() == "discover":
                self._do_discovery(argv[2:])

    def _init_arg_parsers(self) -> None:
        self._main_arg_parser = self._get_main_arg_parser()
        self._discovery_arg_parser = self._get_discovery_arg_parser()

    def _get_main_arg_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument()

        return parser

    def _get_discovery_arg_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument()

        return parser

    def _do_discovery(self, argv: List[str]) -> None:
        self.start = "."
        self.pattern = "bench*.py"

        if argv is not None:
            self._discovery_arg_parser.parse_args(argv, self)

        self.create_benches(from_discovery=True)

    def create_benches(self, from_discovery: bool = False) -> None:
        if from_discovery:
            self.bench = self.loader.discover(self.start, self.pattern)
        else:
            self.bench = self.loader.load_tests_from_module(self.module)

    def run_benchmarks(self) -> None:
        pass


main = BenchmarkProgram
