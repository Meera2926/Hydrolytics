from src.analytics/water_balance_audit import compute_water_balance

def test_water_balance_nrw_calculation():
    res = compute_water_balance(10000, 8500)
    assert res['non_revenue_water_liters'] == 1500
    assert res['loss_percentage'] == 15.0
    assert res['is_acceptable'] is False
