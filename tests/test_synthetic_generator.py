from src.data/synthetic_generator import generate_synthetic_telemetry

def test_generates_synthetic_records():
    recs = generate_synthetic_telemetry(5)
    assert len(recs) == 5
    assert 'flow_rate' in recs[0]
