from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DataType:
    name: str
    bitwidth: int


I16 = DataType(name="i16", bitwidth=16)
I32 = DataType(name="i32", bitwidth=32)
