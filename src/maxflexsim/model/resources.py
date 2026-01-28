from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AreaCost:
    units: float

    def __add__(self, other: "AreaCost") -> "AreaCost":
        return AreaCost(self.units + other.units)

    def fits_within(self, budget: "AreaCost") -> bool:
        return self.units <= budget.units


@dataclass(frozen=True)
class TimingCost:
    delay_ns: float

    def __add__(self, other: "TimingCost") -> "TimingCost":
        return TimingCost(self.delay_ns + other.delay_ns)

    def fits_within(self, budget: "TimingCost") -> bool:
        return self.delay_ns <= budget.delay_ns


@dataclass(frozen=True)
class BandwidthCost:
    bits_per_cycle: float

    def __add__(self, other: "BandwidthCost") -> "BandwidthCost":
        return BandwidthCost(self.bits_per_cycle + other.bits_per_cycle)

    def fits_within(self, budget: "BandwidthCost") -> bool:
        return self.bits_per_cycle <= budget.bits_per_cycle


@dataclass(frozen=True)
class PowerCost:
    watts: float

    def __add__(self, other: "PowerCost") -> "PowerCost":
        return PowerCost(self.watts + other.watts)

    def fits_within(self, budget: "PowerCost") -> bool:
        return self.watts <= budget.watts
