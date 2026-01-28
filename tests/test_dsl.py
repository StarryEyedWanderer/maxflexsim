from maxflexsim.dsl.lower import lower
from maxflexsim.dsl.parser import parse


def test_parse_and_lower():
    program = parse("a,b: i16\ny = add(a,b)\n@latency(y) <= 5 ns\n")
    graph = lower(program)
    assert "output_y" in graph.nodes
    assert any(edge.dst == "output_y" for edge in graph.edges)
    node = graph.nodes["output_y"]
    assert any(constraint.kind == "latency" for constraint in node.constraints)
