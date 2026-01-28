from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from maxflexsim.fabric.fabric import Fabric
from maxflexsim.fabric.link import Link
from maxflexsim.ir.graph import Graph


@dataclass
class RoutingResult:
    graph: Graph
    link_usage: dict[tuple[tuple[int, int], tuple[int, int]], Link]


def _manhattan_path(src: tuple[int, int], dst: tuple[int, int]) -> list[tuple[int, int]]:
    x0, y0 = src
    x1, y1 = dst
    path = [(x0, y0)]
    x = x0
    y = y0
    while x != x1:
        x += 1 if x1 > x else -1
        path.append((x, y))
    while y != y1:
        y += 1 if y1 > y else -1
        path.append((x, y))
    return path


def route(
    graph: Graph, fabric: Fabric, default_capacity: float | None = None
) -> RoutingResult:
    link_usage: dict[tuple[tuple[int, int], tuple[int, int]], Link] = {}
    capacity = (
        fabric.routing.local.capacity_bits_per_cycle
        if default_capacity is None
        else default_capacity
    )
    for edge in graph.edges:
        src_meta = graph.nodes[edge.src].metadata.get("placement")
        dst_meta = graph.nodes[edge.dst].metadata.get("placement")
        if not isinstance(src_meta, dict) or not isinstance(dst_meta, dict):
            raise ValueError("Placement missing for routing")
        src_placement = cast(dict[str, int], src_meta)
        dst_placement = cast(dict[str, int], dst_meta)
        src = (src_placement["x"], src_placement["y"])
        dst = (dst_placement["x"], dst_placement["y"])
        path = _manhattan_path(src, dst)
        hops = 0
        latency = 0.0
        for i in range(len(path) - 1):
            hop = (path[i], path[i + 1])
            link = link_usage.setdefault(hop, Link(capacity_bits_per_cycle=capacity))
            link.add_usage(edge.rate_bits_per_cycle)
            congestion = link.congestion_factor()
            latency += fabric.routing.local.delay_per_hop * congestion
            hops += 1
        edge.metadata["path"] = path
        edge.metadata["hops"] = hops
        edge.metadata["latency"] = latency
    return RoutingResult(graph=graph, link_usage=link_usage)
