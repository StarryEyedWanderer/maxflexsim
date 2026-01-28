from __future__ import annotations

from dataclasses import dataclass

from maxflexsim.ir.graph import Graph


@dataclass
class NormalizeResult:
    graph: Graph


def normalize(graph: Graph) -> NormalizeResult:
    # For MVP we simply ensure deterministic ordering by re-inserting nodes sorted by id.
    ordered = sorted(graph.nodes.values(), key=lambda n: n.id)
    new_graph = Graph()
    for node in ordered:
        new_graph.add_node(node)
    for edge in graph.edges:
        new_graph.add_edge(edge)
    return NormalizeResult(graph=new_graph)
