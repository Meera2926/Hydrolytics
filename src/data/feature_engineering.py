import pandas as pd

def extract_temporal_features(df, timestamp_col='Timestamp'):
    df_copy = df.copy()
    if timestamp_col in df_copy.columns:
        dt = pd.to_datetime(df_copy[timestamp_col])
        df_copy['Hour'] = dt.dt.hour
        df_copy['DayOfWeek'] = dt.dt.dayofweek
        df_copy['IsWeekend'] = df_copy['DayOfWeek'].isin([5, 6]).astype(int)
    return df_copy
