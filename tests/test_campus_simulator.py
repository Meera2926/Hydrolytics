from src.simulator/campus_event_simulator import apply_event_demand_multiplier

def test_applies_festival_demand_surge():
    assert apply_event_demand_multiplier(100.0, 'CULTURAL_FEST') == 165.0
    assert apply_event_demand_multiplier(100.0, 'SEMESTER_BREAK') == 30.0
