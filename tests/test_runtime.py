from pathlib import Path

from maxflexsim.compiler.emit_config import emit_config
from maxflexsim.compiler.impl_select import select_impl
from maxflexsim.compiler.normalize import normalize
from maxflexsim.compiler.place import place
from maxflexsim.dsl.lower import lower
from maxflexsim.dsl.parser import parse_file
from maxflexsim.fabric.fabric import Fabric
from maxflexsim.runtime.runtime import Runtime


def test_runtime_capability_map(tmp_path: Path):
    fabric = Fabric.from_json(Path("fabric/examples/fabric_small.json"))
    program = parse_file(Path("examples/adder.mfs"))
    graph = select_impl(normalize(lower(program)).graph).graph
    placement = place(graph, fabric)
    emit_config(placement.graph, fabric, tmp_path)
    runtime = Runtime.load(fabric, tmp_path / "config.json")
    caps = runtime.get_capability_map()
    assert sum(caps.free_tiles_per_island.values()) < fabric.width * fabric.height
