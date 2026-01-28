from __future__ import annotations

from dataclasses import dataclass

from maxflexsim.ir.constraints import Constraint
from maxflexsim.ir.types import DataType


@dataclass
class Node:
    id: str
    op_type: str
    dtype: DataType
    shape: tuple[int, ...]
    constraints: list[Constraint]
    impl_choices: list[str]
    metadata: dict[str, object]


@dataclass
class Edge:
    src: str
    dst: str
    bitwidth: int
    rate_bits_per_cycle: float
    latency_req: float | None
    metadata: dict[str, object]
