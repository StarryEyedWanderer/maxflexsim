from pathlib import Path

from maxflexsim.compiler.emit_certificate import emit_certificate
from maxflexsim.compiler.emit_config import emit_config
from maxflexsim.compiler.impl_select import select_impl
from maxflexsim.compiler.normalize import normalize
from maxflexsim.compiler.place import place
from maxflexsim.compiler.route_local import route
from maxflexsim.dsl.lower import lower
from maxflexsim.dsl.parser import parse_file
from maxflexsim.fabric.fabric import Fabric


def test_compile_smoke(tmp_path: Path):
    fabric = Fabric.from_json(Path("fabric/examples/fabric_small.json"))
    program = parse_file(Path("examples/adder.mfs"))
    graph = lower(program)
    graph = normalize(graph).graph
    graph = select_impl(graph).graph
    placement = place(graph, fabric)
    routing = route(placement.graph, fabric)
    emit_config(graph, fabric, tmp_path)
    emit_certificate(graph, fabric, routing.link_usage, tmp_path)
    config = (tmp_path / "config.json").read_text(encoding="utf-8")
    cert = (tmp_path / "certificate.json").read_text(encoding="utf-8")
    assert fabric.fingerprint in config
    assert fabric.fingerprint in cert
