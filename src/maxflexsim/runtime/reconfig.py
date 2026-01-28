from __future__ import annotations

from dataclasses import dataclass

from maxflexsim.runtime.runtime import Runtime


@dataclass
class ReconfigResult:
    cost: int


def swap_island(
    runtime: Runtime, island_id: str, new_placements: dict[str, dict[str, int]]
) -> ReconfigResult:
    runtime.placements = {
        node: placement
        for node, placement in runtime.placements.items()
        if runtime.fabric.island_for_tile(placement["x"], placement["y"]).id != island_id
    }
    for node, placement in new_placements.items():
        if runtime.fabric.island_for_tile(placement["x"], placement["y"]).id != island_id:
            continue
        runtime.placements[node] = placement
    cost = runtime.fabric.island_width * runtime.fabric.island_height
    return ReconfigResult(cost=cost)
