from src.storage/tank_level_tracker import compute_tank_volume_liters

def test_tank_volume_calculations():
    res = compute_tank_volume_liters(15.0, 50000)
    assert res['current_volume_liters'] == 7500.0
    assert res['is_low'] is True
    assert res['is_critical_overflow'] is False
