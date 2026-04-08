import os
from src.data.dataset_loader import load_campus_dataset

def test_dataset_loader_reads_csv():
    if os.path.exists('hydrolytix_dataset.csv'):
        df = load_campus_dataset('hydrolytix_dataset.csv')
        assert not df.empty
        assert len(df.columns) > 0
