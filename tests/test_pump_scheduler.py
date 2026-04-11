from src.optimizer/pump_scheduler import get_optimal_pump_schedule

def test_avoids_pumping_during_peak_tariff():
    sched = get_optimal_pump_schedule([8, 18])
    assert sched[8] == 'OFF'
    assert sched[18] == 'OFF'
    assert sched[2] == 'ON'
