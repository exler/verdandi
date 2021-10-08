from dataclasses import dataclass
from enum import IntEnum
from typing import List, Optional

from verdandi.utils import print_header


class ResultType(IntEnum):
    OK = 1
    ERROR = 2


@dataclass(eq=False, order=False, frozen=True)
class BenchmarkResult:
    name: str

    rtype: ResultType

    # Memory taken in seconds
    duration_sec: Optional[float]

    # Memory allocated in bytes
    memory_diff: Optional[float]

    # Captured stdout
    stdout: List[List[str]]

    def print_result(self) -> None:
        print(
            f"{self.name} - duration (sec): {round(self.duration_sec, 4)}, memory allocated (bytes): {self.memory_diff}"
        )

    def print_stdout(self) -> None:
        for iter_index, iter_output in enumerate(self.stdout):
            print_header(f"{self.name}: iteration {iter_index}", padding_symbol="-")
            for output in iter_output:
                print(output)
