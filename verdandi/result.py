from dataclasses import dataclass
from enum import IntEnum
from typing import List

from verdandi.cli import print_header


class ResultType(IntEnum):
    OK = 1
    ERROR = 2


@dataclass(eq=False, order=False, frozen=True)
class BenchmarkResult:
    name: str

    rtype: ResultType

    # Memory taken in seconds
    duration_sec: float

    # Memory allocated in bytes
    memory_diff: float

    # Captured stream outputs
    stdout: List[str]
    stderr: List[str]

    # Captured exceptions
    exceptions: List[Exception]

    def __str__(self) -> str:
        msg = f"{self.name} ({self.rtype.name})"
        msg += f" - duration (sec): {round(self.duration_sec, 4)}, memory allocated (bytes): {self.memory_diff}"
        return msg

    def print_stdout(self) -> None:
        for iter_index, iter_stdout in enumerate(self.stdout):
            if not iter_stdout:
                continue

            print_header(f"{self.name}: iteration {iter_index}", padding_symbol="-")
            print(iter_stdout)

    def print_stderr(self) -> None:
        for iter_index, iter_stderr in enumerate(self.stderr):
            if not iter_stderr:
                continue

            print_header(f"{self.name}: iteration {iter_index}", padding_symbol="-")
            print(iter_stderr)

    def print_exceptions(self) -> None:
        for iter_index, iter_exc in enumerate(self.exceptions):
            print_header(f"{self.name}: iteration {iter_index}", padding_symbol="-")
            print(f"{iter_exc.__class__.__name__}: {str(iter_exc)}")
