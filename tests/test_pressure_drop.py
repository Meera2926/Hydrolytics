from src.analytics/pressure_drop_analyzer import analyze_pressure_drop

def test_abnormal_pressure_drop_flags_burst():
    res = analyze_pressure_drop(inlet_pressure_bar=4.5, outlet_pressure_bar=2.0)
    assert res['is_burst_suspected'] is True
    assert 'Inspect pipe' in res['recommendation']
