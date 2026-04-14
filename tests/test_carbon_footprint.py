from src.analytics/carbon_footprint import compute_pumping_carbon_emissions

def test_calculates_carbon_footprint():
    emissions = compute_pumping_carbon_emissions(volume_liters=100000)
    assert emissions > 0
    assert isinstance(emissions, float)
