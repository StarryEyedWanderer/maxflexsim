import pytest

from maxflexsim.ir.graph import Graph
from maxflexsim.ir.ops import Edge, Node
from maxflexsim.ir.types import I16


def _node(node_id: str) -> Node:
    return Node(
        id=node_id,
        op_type="ADD",
        dtype=I16,
        shape=(),
        constraints=[],
        impl_choices=["add_small"],
        metadata={},
    )


def test_topological_order():
    graph = Graph()
    graph.add_node(_node("a"))
    graph.add_node(_node("b"))
    graph.add_edge(
        Edge(
            src="a",
            dst="b",
            bitwidth=16,
            rate_bits_per_cycle=16.0,
            latency_req=None,
            metadata={},
        )
    )
    order = graph.topological_order()
    assert order == ["a", "b"]


def test_cycle_detection():
    graph = Graph()
    graph.add_node(_node("a"))
    graph.add_node(_node("b"))
    graph.add_edge(
        Edge(
            src="a",
            dst="b",
            bitwidth=16,
            rate_bits_per_cycle=16.0,
            latency_req=None,
            metadata={},
        )
    )
    graph.add_edge(
        Edge(
            src="b",
            dst="a",
            bitwidth=16,
            rate_bits_per_cycle=16.0,
            latency_req=None,
            metadata={},
        )
    )
    with pytest.raises(ValueError):
        graph.topological_order()
