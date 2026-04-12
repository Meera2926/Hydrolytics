from src.analytics/per_capita_usage import calculate_lpcd

def test_lpcd_compliance():
    res = calculate_lpcd(total_daily_liters=60000, student_population=500)
    assert res['lpcd'] == 120.0
    assert res['is_compliant'] is True
