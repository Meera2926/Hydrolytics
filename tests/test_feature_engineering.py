import pandas as pd
from src.data.feature_engineering import extract_temporal_features

def test_extract_temporal_features():
    df = pd.DataFrame({'Timestamp': ['2026-04-09 14:30:00']})
    res = extract_temporal_features(df)
    assert res['Hour'].iloc[0] == 14
    assert res['IsWeekend'].iloc[0] == 0
