import json
from datetime import datetime

def format_telemetry_log(zone, flow_rate, status="OK"):
    return json.dumps({
        'timestamp': datetime.utcnow().isoformat(),
        'zone': zone,
        'flow_rate': flow_rate,
        'status': status
    })
