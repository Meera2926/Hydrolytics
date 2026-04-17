def get_seasonal_multiplier(month):
    # Summer months (March to May) experience higher evaporative demand
    if month in [3, 4, 5]: return 1.35
    if month in [7, 8, 9]: return 0.90 # Monsoon
    return 1.05
