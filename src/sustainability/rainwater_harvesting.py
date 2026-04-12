def estimate_rainwater_yield_liters(catchment_area_sq_m, rainfall_mm, runoff_coeff=0.85):
    # Yield (L) = Area (m2) * Rainfall (mm) * Runoff Coefficient
    return round(catchment_area_sq_m * rainfall_mm * runoff_coeff, 1)
