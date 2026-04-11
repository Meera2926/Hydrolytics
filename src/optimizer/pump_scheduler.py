def get_optimal_pump_schedule(peak_hours=[8, 9, 10, 18, 19, 20]):
    schedule = {}
    for hour in range(24):
        schedule[hour] = 'OFF' if hour in peak_hours else 'ON'
    return schedule
