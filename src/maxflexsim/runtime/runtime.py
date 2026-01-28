from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from maxflexsim.fabric.fabric import Fabric
from maxflexsim.runtime.capability_map import CapabilityMap


@dataclass
class Runtime:
    fabric: Fabric
    placements: dict[str, dict[str, int]]

    @classmethod
    def load(cls, fabric: Fabric, config_path: str | Path) -> "Runtime":
        payload = json.loads(Path(config_path).read_text(encoding="utf-8"))
        return cls(fabric=fabric, placements=payload.get("placements", {}))

    def get_capability_map(self) -> CapabilityMap:
        free_tiles: dict[str, int] = {}
        total_tiles: dict[str, int] = {}
        for island in self.fabric.islands():
            total_tiles[island.id] = island.width * island.height
            free_tiles[island.id] = island.width * island.height
        for placement in self.placements.values():
            island_id = self.fabric.island_for_tile(placement["x"], placement["y"]).id
            free_tiles[island_id] -= 1
        fmax = {island_id: 1.0 for island_id in total_tiles}
        return CapabilityMap(
            free_tiles_per_island=free_tiles,
            fmax_per_island=fmax,
            noc_headroom=self.fabric.noc.link_bandwidth,
        )

    def step(self) -> dict[str, float]:
        return {"power_watts": 0.0, "traffic_bits": 0.0}
