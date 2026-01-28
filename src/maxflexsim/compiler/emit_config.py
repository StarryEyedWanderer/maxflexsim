from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from maxflexsim.fabric.fabric import Fabric
from maxflexsim.ir.graph import Graph


@dataclass
class EmitConfigResult:
    path: Path


def emit_config(graph: Graph, fabric: Fabric, out_dir: str | Path) -> EmitConfigResult:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    payload = {
        "fabric_fingerprint": fabric.fingerprint,
        "placements": {
            node_id: node.metadata.get("placement") for node_id, node in graph.nodes.items()
        },
        "routes": [edge.metadata.get("path") for edge in graph.edges],
    }
    config_path = out_path / "config.json"
    config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return EmitConfigResult(path=config_path)
