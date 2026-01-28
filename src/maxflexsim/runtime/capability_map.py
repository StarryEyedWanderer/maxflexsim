from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CapabilityMap:
    free_tiles_per_island: dict[str, int]
    fmax_per_island: dict[str, float]
    noc_headroom: float
