from src.analytics/leak_detector import detect_night_time_leak

def test_detects_leak_when_night_flow_high():
    readings = [
        {'hour': 1, 'flow_rate': 45.0},
        {'hour': 2, 'flow_rate': 42.0},
        {'hour': 3, 'flow_rate': 40.0},
    ]
    res = detect_night_time_leak(readings, leak_threshold=25.0)
    assert res['leak_detected'] is True
    assert res['severity'] == 'MODERATE'
