def compute_tank_volume_liters(fill_percentage, total_capacity_liters):
    fill = max(0.0, min(100.0, fill_percentage))
    current_liters = (fill / 100.0) * total_capacity_liters
    return {
        'current_volume_liters': round(current_liters, 1),
        'headroom_liters': round(total_capacity_liters - current_liters, 1),
        'is_low': fill < 20.0,
        'is_critical_overflow': fill > 95.0
    }
