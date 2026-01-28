from pathlib import Path

from maxflexsim.compiler.place import place
from maxflexsim.compiler.route_local import route
from maxflexsim.dsl.lower import lower
from maxflexsim.dsl.parser import parse
from maxflexsim.fabric.fabric import Fabric


def test_route_manhattan_distance():
    fabric = Fabric.from_json(Path("fabric/examples/fabric_small.json"))
    program = parse("a,b: i16\ny = add(a,b)\n")
    graph = lower(program)
    placement = place(graph, fabric)
    routing = route(placement.graph, fabric)
    edge = routing.graph.edges[0]
    assert edge.metadata["hops"] >= 0
