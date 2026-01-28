from __future__ import annotations

from dataclasses import dataclass

from maxflexsim.fabric.fabric import Fabric
from maxflexsim.model.resources import AreaCost, PowerCost, TimingCost


@dataclass(frozen=True)
class OpImpl:
    name: str
    area: AreaCost
    timing: TimingCost
    power: PowerCost


OP_IMPLEMENTATIONS: dict[str, list[OpImpl]] = {
    "AND": [
        OpImpl("and_small", AreaCost(1.0), TimingCost(1.0), PowerCost(0.1)),
        OpImpl("and_fast", AreaCost(1.5), TimingCost(0.6), PowerCost(0.15)),
    ],
    "XOR": [
        OpImpl("xor_small", AreaCost(1.1), TimingCost(1.2), PowerCost(0.12)),
        OpImpl("xor_fast", AreaCost(1.7), TimingCost(0.7), PowerCost(0.18)),
    ],
    "ADD": [
        OpImpl("add_small", AreaCost(2.0), TimingCost(2.5), PowerCost(0.2)),
        OpImpl("add_fast", AreaCost(3.0), TimingCost(1.5), PowerCost(0.3)),
    ],
    "MUL": [
        OpImpl("mul_small", AreaCost(4.0), TimingCost(4.5), PowerCost(0.5)),
        OpImpl("mul_fast", AreaCost(6.0), TimingCost(2.8), PowerCost(0.7)),
    ],
    "REG": [
        OpImpl("reg_small", AreaCost(0.5), TimingCost(0.2), PowerCost(0.05)),
        OpImpl("reg_fast", AreaCost(0.8), TimingCost(0.1), PowerCost(0.08)),
    ],
    "MUX": [
        OpImpl("mux_small", AreaCost(1.2), TimingCost(1.1), PowerCost(0.12)),
        OpImpl("mux_fast", AreaCost(1.8), TimingCost(0.7), PowerCost(0.18)),
    ],
    "CONST": [
        OpImpl("const_small", AreaCost(0.2), TimingCost(0.1), PowerCost(0.02)),
        OpImpl("const_fast", AreaCost(0.3), TimingCost(0.05), PowerCost(0.03)),
    ],
    "INPUT": [
        OpImpl("input_small", AreaCost(0.4), TimingCost(0.2), PowerCost(0.04)),
        OpImpl("input_fast", AreaCost(0.6), TimingCost(0.1), PowerCost(0.05)),
    ],
    "OUTPUT": [
        OpImpl("output_small", AreaCost(0.4), TimingCost(0.2), PowerCost(0.04)),
        OpImpl("output_fast", AreaCost(0.6), TimingCost(0.1), PowerCost(0.05)),
    ],
}


def estimate_cost(op_type: str, impl_name: str, fabric: Fabric) -> TimingCost:
    """Return a timing cost for selecting impl on a given fabric.

    This MVP model uses implementation timing directly and ignores fabric scaling,
    but it still receives fabric for future extension.
    """
    impls = OP_IMPLEMENTATIONS.get(op_type, [])
    for impl in impls:
        if impl.name == impl_name:
            return impl.timing
    raise ValueError(f"Unknown implementation {impl_name} for op {op_type}")
