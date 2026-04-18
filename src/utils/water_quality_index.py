def evaluate_water_potability(ph, turbidity_ntu, tds_ppm):
    is_ph_safe = 6.5 <= ph <= 8.5
    is_turbidity_safe = turbidity_ntu <= 5.0
    is_tds_safe = tds_ppm <= 500
    return {
        'is_potable': is_ph_safe and is_turbidity_safe and is_tds_safe,
        'status': 'POTABLE' if (is_ph_safe and is_turbidity_safe and is_tds_safe) else 'TREATMENT_REQUIRED'
    }
