from src.analytics/pipeline_health_score import compute_pipeline_health_score

def test_pipeline_health_scoring():
    score = compute_pipeline_health_score(leak_count_30d=1, avg_pressure_bar=4.0, pipe_age_years=5)
    assert score == 92
