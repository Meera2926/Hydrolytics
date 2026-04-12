from src.storage/overflow_prevention import OverflowSafetySwitch

def test_overflow_switch_hysteresis():
    switch = OverflowSafetySwitch(high_cutoff_pct=90.0, low_restart_pct=80.0)
    assert switch.update_level(91.0) is False
    assert switch.update_level(85.0) is False  # stays off
    assert switch.update_level(79.0) is True   # turns back on
