from pathlib import Path

from maxflexsim.compiler.emit_config import emit_config
from maxflexsim.compiler.impl_select import select_impl
from maxflexsim.compiler.normalize import normalize
from maxflexsim.compiler.place import place
from maxflexsim.dsl.lower import lower
from maxflexsim.dsl.parser import parse_file
from maxflexsim.fabric.fabric import Fabric
from maxflexsim.viz.viewer import render_heatmap


def test_viewer_renders(tmp_path: Path):
    fabric = Fabric.from_json(Path("fabric/examples/fabric_small.json"))
    program = parse_file(Path("examples/adder.mfs"))
    graph = select_impl(normalize(lower(program)).graph).graph
    placement = place(graph, fabric)
    emit_config(placement.graph, fabric, tmp_path)
    out_path = render_heatmap(fabric, tmp_path / "config.json", tmp_path / "heatmap.png")
    assert out_path.exists()
    assert out_path.stat().st_size > 0
