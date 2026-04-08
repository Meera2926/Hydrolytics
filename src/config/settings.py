import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'hydrolytics-campus-secure-key-2026')
    DATASET_PATH = os.getenv('DATASET_PATH', 'hydrolytix_dataset.csv')
    MODEL_PATH = os.getenv('MODEL_PATH', 'xgboost_model.pkl')
    DEFAULT_LEAK_THRESHOLD_L_PER_MIN = 25.0
    NIGHT_HOURS = [0, 1, 2, 3, 4]
