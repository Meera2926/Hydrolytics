def compute_campus_kpis(hourly_data):
    if not hourly_data: return {}
    flows = [d['flow_rate'] for d in hourly_data]
    return {
        'total_volume_liters': sum(flows) * 60,
        'peak_flow_rate_lpm': max(flows),
        'min_flow_rate_lpm': min(flows),
        'average_flow_rate_lpm': round(sum(flows) / len(flows), 1)
    }
