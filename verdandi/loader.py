import importlib
import inspect
import os
import types
from fnmatch import fnmatch
from pathlib import Path
from typing import List, Type, Union

from verdandi.benchmark import Benchmark
from verdandi.utils import convert_name


class BenchmarkLoader:
    method_prefix = "bench_"

    def load_benches_from_module(self, module: types.ModuleType) -> List[Type[Benchmark]]:
        benches: List[Type[Benchmark]] = []

        for _, obj in inspect.getmembers(module):
            if isinstance(obj, type) and issubclass(obj, Benchmark) and obj is not Benchmark:
                benches.append(obj)

        return benches

    def load_benches_from_name(self, name: str) -> List[Type[Benchmark]]:
        try:
            module = importlib.import_module(name)
        except (TypeError, ImportError):
            # Dotted filename or no such module
            return []

        return self.load_benches_from_module(module)

    def discover(self, start_dir: Union[Path, str], pattern="bench_*.py") -> List[Type[Benchmark]]:
        """
        Find and return all benchmarks from the specified start directory,
        recursing into subsequent directories.
        """

        benches: List[Type[Benchmark]] = []

        with os.scandir(start_dir) as iterator:
            for entry in iterator:
                if entry.is_dir(follow_symlinks=False):
                    benches.extend(self.discover(start_dir=entry.path, pattern=pattern))
                elif entry.is_file(follow_symlinks=False) and fnmatch(entry.name, pattern):
                    path = convert_name(entry.path)
                    benches.extend(self.load_benches_from_name(path))

        return benches
