from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Link:
    capacity_bits_per_cycle: float
    utilization_bits_per_cycle: float = 0.0

    def add_usage(self, amount: float) -> None:
        self.utilization_bits_per_cycle += amount

    def is_congested(self) -> bool:
        return self.utilization_bits_per_cycle > self.capacity_bits_per_cycle

    def congestion_factor(self) -> float:
        if self.capacity_bits_per_cycle <= 0:
            return float("inf")
        return max(1.0, self.utilization_bits_per_cycle / self.capacity_bits_per_cycle)
