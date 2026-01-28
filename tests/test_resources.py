from maxflexsim.model.resources import AreaCost, BandwidthCost, PowerCost, TimingCost


def test_resource_arithmetic_and_budget():
    area = AreaCost(1.0) + AreaCost(2.0)
    assert area.units == 3.0
    assert area.fits_within(AreaCost(3.1))

    timing = TimingCost(1.2) + TimingCost(0.3)
    assert timing.delay_ns == 1.5
    assert timing.fits_within(TimingCost(2.0))

    bandwidth = BandwidthCost(10.0) + BandwidthCost(5.0)
    assert bandwidth.bits_per_cycle == 15.0
    assert bandwidth.fits_within(BandwidthCost(20.0))

    power = PowerCost(0.5) + PowerCost(0.2)
    assert power.watts == 0.7
    assert power.fits_within(PowerCost(1.0))
