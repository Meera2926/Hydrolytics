from src.reports/summary_metrics import compute_campus_kpis

def test_computes_kpis():
    data = [{'flow_rate': 20.0}, {'flow_rate': 40.0}]
    kpis = compute_campus_kpis(data)
    assert kpis['peak_flow_rate_lpm'] == 40.0
    assert kpis['min_flow_rate_lpm'] == 20.0
