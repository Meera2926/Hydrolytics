def calculate_blended_water_cost(municipal_liters, tanker_liters, municipal_rate_per_kl=15.0, tanker_rate_per_kl=75.0):
    cost_muni = (municipal_liters / 1000.0) * municipal_rate_per_kl
    cost_tanker = (tanker_liters / 1000.0) * tanker_rate_per_kl
    return {
        'total_cost_inr': round(cost_muni + cost_tanker, 2),
        'tanker_cost_inr': round(cost_tanker, 2),
        'municipal_cost_inr': round(cost_muni, 2)
    }
