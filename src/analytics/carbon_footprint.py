def compute_pumping_carbon_emissions(volume_liters, head_meters=30.0, grid_factor_kg_per_kwh=0.82):
    # Energy (kWh) = (Volume (m3) * Head (m) * 9.81) / (3600 * pump_efficiency)
    volume_m3 = volume_liters / 1000.0
    kwh = (volume_m3 * head_meters * 9.81) / (3600 * 0.70)
    co2_kg = kwh * grid_factor_kg_per_kwh
    return round(co2_kg, 2)
