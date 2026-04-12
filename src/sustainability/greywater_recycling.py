def calculate_greywater_recovery(hostel_inflow_liters, recovery_efficiency=0.65):
    return round(hostel_inflow_liters * recovery_efficiency, 1)
