from __future__ import annotations

import json
from pathlib import Path

from maxflexsim.fabric.fabric import Fabric


def render_heatmap(fabric: Fabric, config_path: str | Path, out_path: str | Path) -> Path:
    payload = json.loads(Path(config_path).read_text(encoding="utf-8"))
    placements = payload.get("placements", {})
    grid = [[0 for _ in range(fabric.width)] for _ in range(fabric.height)]
    for placement in placements.values():
        grid[placement["y"]][placement["x"]] = 1
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# MaxFlexSim placement heatmap (textual)"]
    for row in grid:
        lines.append("".join("#" if cell else "." for cell in row))
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
