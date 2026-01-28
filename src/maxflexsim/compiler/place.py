from __future__ import annotations

from dataclasses import dataclass

from maxflexsim.fabric.fabric import Fabric
from maxflexsim.ir.graph import Graph


@dataclass
class PlacementResult:
    graph: Graph
    placements: dict[str, tuple[int, int]]


def place(graph: Graph, fabric: Fabric) -> PlacementResult:
    placements: dict[str, tuple[int, int]] = {}
    tiles = list(fabric.tiles())
    if len(graph.nodes) > len(tiles):
        raise ValueError(
            f"Out of tiles: need {len(graph.nodes)} but fabric has {len(tiles)} tiles"
        )
    for node, tile in zip(graph.nodes.values(), tiles, strict=False):
        placements[node.id] = (tile.x, tile.y)
        node.metadata["placement"] = {"x": tile.x, "y": tile.y}
        node.metadata["island"] = fabric.island_for_tile(tile.x, tile.y).id
    return PlacementResult(graph=graph, placements=placements)
