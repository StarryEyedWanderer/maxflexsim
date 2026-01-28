from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Constraint:
    kind: str
    value: float | str


@dataclass(frozen=True)
class LatencyConstraint(Constraint):
    def __init__(self, value_ns: float) -> None:
        super().__init__(kind="latency", value=value_ns)


@dataclass(frozen=True)
class LocalityConstraint(Constraint):
    def __init__(self, value: str) -> None:
        super().__init__(kind="locality", value=value)
