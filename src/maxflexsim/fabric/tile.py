from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Tile:
    x: int
    y: int
    capacity: int
