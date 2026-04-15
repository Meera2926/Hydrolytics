import random

def generate_synthetic_telemetry(num_records=10):
    records = []
    for i in range(num_records):
        records.append({
            'hour': i % 24,
            'flow_rate': round(random.uniform(15.0, 85.0), 2),
            'pressure': round(random.uniform(3.0, 5.0), 2)
        })
    return records
