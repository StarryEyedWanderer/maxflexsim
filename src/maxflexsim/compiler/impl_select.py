from __future__ import annotations

from dataclasses import dataclass

from maxflexsim.ir.constraints import LatencyConstraint
from maxflexsim.ir.graph import Graph
from maxflexsim.ir.oplib import OP_IMPLEMENTATIONS


@dataclass
class ImplSelectResult:
    graph: Graph


def select_impl(graph: Graph) -> ImplSelectResult:
    for node in graph.nodes.values():
        impls = OP_IMPLEMENTATIONS.get(node.op_type, [])
        if not impls:
            raise ValueError(f"No implementations for op {node.op_type}")
        latency_req: float | None = None
        for constraint in node.constraints:
            if isinstance(constraint, LatencyConstraint):
                if isinstance(constraint.value, float):
                    latency_req = constraint.value
        chosen = None
        for impl in sorted(impls, key=lambda imp: imp.area.units):
            if latency_req is None or impl.timing.delay_ns <= latency_req:
                chosen = impl
                break
        if chosen is None:
            chosen = min(impls, key=lambda imp: imp.timing.delay_ns)
        node.metadata["impl"] = chosen.name
    return ImplSelectResult(graph=graph)
