import json

from maxflexsim.compiler.emit_certificate import emit_certificate
from maxflexsim.compiler.route_local import route
from maxflexsim.fabric.fabric import Fabric
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


def test_congestion_and_bandwidth_reporting(tmp_path):
    fabric = Fabric.from_json("fabric/examples/fabric_small.json")
    graph = Graph()
    graph.add_node(_node("src"))
    graph.add_node(_node("dst"))
    graph.nodes["src"].metadata["placement"] = {"x": 0, "y": 0}
    graph.nodes["dst"].metadata["placement"] = {"x": 1, "y": 0}
    for _ in range(3):
        graph.add_edge(
            Edge(
                src="src",
                dst="dst",
                bitwidth=16,
                rate_bits_per_cycle=16.0,
                latency_req=None,
                metadata={},
            )
        )
    routing = route(graph, fabric, default_capacity=16.0)
    result = emit_certificate(graph, fabric, routing.link_usage, tmp_path)
    payload = json.loads(result.path.read_text(encoding="utf-8"))
    assert payload["congested_links"]
    assert payload["bandwidth"]["max_link_utilization"] >= 1.0
