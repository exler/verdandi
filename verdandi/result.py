from dataclasses import dataclass


@dataclass(eq=False, order=False, frozen=True)
class BenchmarkResult:
    name: str
    duration_sec: float = 0.0
