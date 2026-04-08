import os
import pandas as pd

def load_campus_dataset(filepath='hydrolytix_dataset.csv'):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}")
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()
    return df
