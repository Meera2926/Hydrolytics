from src.sustainability/greywater_recycling import calculate_greywater_recovery

def test_greywater_recovery_rate():
    recovered = calculate_greywater_recovery(10000, 0.65)
    assert recovered == 6500.0
