from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from maxflexsim.fabric.fabric import Fabric
from maxflexsim.fabric.link import Link
from maxflexsim.ir.constraints import LatencyConstraint
from maxflexsim.ir.graph import Graph
from maxflexsim.ir.oplib import OP_IMPLEMENTATIONS
from maxflexsim.model.resources import AreaCost


@dataclass
class EmitCertificateResult:
    path: Path


def _impl_area(op_type: str, impl_name: str) -> float:
    for impl in OP_IMPLEMENTATIONS.get(op_type, []):
        if impl.name == impl_name:
            return impl.area.units
    return 0.0


def emit_certificate(
    graph: Graph,
    fabric: Fabric,
    link_usage: dict[tuple[tuple[int, int], tuple[int, int]], Link],
    out_dir: str | Path,
) -> EmitCertificateResult:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    total_area = AreaCost(0.0)
    constraints_report: list[dict[str, object]] = []
    for node in graph.nodes.values():
        impl_name = node.metadata.get("impl", "")
        total_area += AreaCost(_impl_area(node.op_type, str(impl_name)))
        for constraint in node.constraints:
            if isinstance(constraint, LatencyConstraint) and isinstance(constraint.value, float):
                def _latency(edge_value: object) -> float:
                    if isinstance(edge_value, (int, float)):
                        return float(edge_value)
                    return 0.0

                observed = max(
                    (
                        _latency(edge.metadata.get("latency", 0.0))
                        for edge in graph.incoming(node.id)
                    ),
                    default=0.0,
                )
                constraints_report.append(
                    {
                        "node": node.id,
                        "kind": "latency",
                        "limit": constraint.value,
                        "observed": observed,
                        "pass": observed <= constraint.value,
                    }
                )

    edge_latencies = [
        {
            "src": edge.src,
            "dst": edge.dst,
            "latency": edge.metadata.get("latency", 0.0),
            "hops": edge.metadata.get("hops", 0),
        }
        for edge in graph.edges
    ]
    total_demand = sum(edge.rate_bits_per_cycle for edge in graph.edges)
    max_utilization = 0.0
    if link_usage:
        max_utilization = max(
            link.utilization_bits_per_cycle / link.capacity_bits_per_cycle
            if link.capacity_bits_per_cycle > 0
            else float("inf")
            for link in link_usage.values()
        )
    congested = [
        {
            "link": f"{src}->{dst}",
            "utilization": link.utilization_bits_per_cycle,
            "capacity": link.capacity_bits_per_cycle,
        }
        for (src, dst), link in link_usage.items()
        if link.is_congested()
    ]
    payload = {
        "fabric_fingerprint": fabric.fingerprint,
        "total_area": total_area.units,
        "edge_latencies": edge_latencies,
        "bandwidth": {
            "total_demand_bits_per_cycle": total_demand,
            "max_link_utilization": max_utilization,
        },
        "constraints": constraints_report,
        "congested_links": congested,
    }
    cert_path = out_path / "certificate.json"
    cert_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return EmitCertificateResult(path=cert_path)
