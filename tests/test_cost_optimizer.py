from src.optimizer/cost_optimizer import calculate_blended_water_cost

def test_computes_blended_water_cost():
    res = calculate_blended_water_cost(municipal_liters=50000, tanker_liters=10000)
    assert res['municipal_cost_inr'] == 750.0
    assert res['tanker_cost_inr'] == 750.0
    assert res['total_cost_inr'] == 1500.0
