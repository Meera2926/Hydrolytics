def detect_night_time_leak(hourly_readings, leak_threshold=25.0):
    night_readings = [r['flow_rate'] for r in hourly_readings if r.get('hour') in [1, 2, 3, 4]]
    if not night_readings:
        return {'leak_detected': False, 'avg_night_flow': 0.0}
    avg_night_flow = sum(night_readings) / len(night_readings)
    return {
        'leak_detected': avg_night_flow > leak_threshold,
        'avg_night_flow': round(avg_night_flow, 2),
        'severity': 'HIGH' if avg_night_flow > leak_threshold * 2 else 'MODERATE' if avg_night_flow > leak_threshold else 'NORMAL'
    }
