def apply_event_demand_multiplier(base_demand, event_type):
    multipliers = {
        'NORMAL': 1.0,
        'CULTURAL_FEST': 1.65,
        'SPORTS_MEET': 1.40,
        'EXAM_PERIOD': 0.85,
        'SEMESTER_BREAK': 0.30
    }
    return round(base_demand * multipliers.get(event_type, 1.0), 1)
