from src.utils.water_units import liters_to_cubic_meters, cubic_meters_to_liters, flow_rate_lpm_to_lps

def test_water_unit_conversions():
    assert liters_to_cubic_meters(5000) == 5.0
    assert cubic_meters_to_liters(3.5) == 3500.0
    assert flow_rate_lpm_to_lps(60.0) == 1.0
