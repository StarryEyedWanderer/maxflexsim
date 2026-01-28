from pathlib import Path

from maxflexsim.fabric.fabric import Fabric


def test_fabric_load_and_island_mapping():
    fabric = Fabric.from_json(Path("fabric/examples/fabric_small.json"))
    assert fabric.width == 16
    assert fabric.height == 16
    island = fabric.island_for_tile(0, 0)
    assert island.row == 0
    assert island.col == 0
    island_br = fabric.island_for_tile(15, 15)
    assert island_br.row == 1
    assert island_br.col == 1
