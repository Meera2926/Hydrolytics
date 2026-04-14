import json
from src.utils/logger import format_telemetry_log

def test_formats_json_telemetry():
    log_str = format_telemetry_log('Academic C', 45.2)
    data = json.loads(log_str)
    assert data['zone'] == 'Academic C'
    assert data['flow_rate'] == 45.2
