import os
from fnmatch import fnmatch
from pathlib import Path
from typing import List, Type, Union

from verdandi.benchmark import Benchmark


class BenchmarkLoader:
    def load_benches_from_file(self, path: Union[Path, str]) -> List[Type[Benchmark]]:
        """
        Find and return all benchmarks from the specified file
        """
        return []

    def load_benches_from_module(self, module) -> List[Type[Benchmark]]:
        return []

    def load_benches_from_name(self, name: str) -> List[Type[Benchmark]]:
        return []

    def discover(self, start_dir: Union[Path, str], pattern="bench*.py") -> List[Type[Benchmark]]:
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
                    benches.extend(self.load_benches_from_file(entry.path))

        return benches
