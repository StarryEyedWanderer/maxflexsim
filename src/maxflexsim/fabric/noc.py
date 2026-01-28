from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NoC:
    router_latency: float
    link_bandwidth: float
