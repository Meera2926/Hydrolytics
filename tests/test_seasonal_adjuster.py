from src.analytics/seasonal_adjuster import get_seasonal_multiplier

def test_seasonal_multiplier():
    assert get_seasonal_multiplier(4) == 1.35
    assert get_seasonal_multiplier(8) == 0.90
