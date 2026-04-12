from src.sustainability/rainwater_harvesting import estimate_rainwater_yield_liters

def test_calculates_rooftop_harvesting_yield():
    yield_liters = estimate_rainwater_yield_liters(catchment_area_sq_m=1000, rainfall_mm=25, runoff_coeff=0.85)
    assert yield_liters == 21250.0
