def compute_pipeline_health_score(leak_count_30d, avg_pressure_bar, pipe_age_years):
    score = 100
    score -= leak_count_30d * 8
    if avg_pressure_bar > 6.0: score -= 15
    if pipe_age_years > 15: score -= 20
    return max(0, min(100, score))
