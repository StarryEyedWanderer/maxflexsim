from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Island:
    row: int
    col: int
    x_start: int
    y_start: int
    width: int
    height: int

    @property
    def id(self) -> str:
        return f"island_{self.row}_{self.col}"

    def contains(self, x: int, y: int) -> bool:
        return (
            self.x_start <= x < self.x_start + self.width
            and self.y_start <= y < self.y_start + self.height
        )
