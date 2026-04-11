def compute_water_balance(total_inflow_liters, metered_outflow_liters):
    non_revenue_water = total_inflow_liters - metered_outflow_liters
    loss_pct = (non_revenue_water / total_inflow_liters) * 100 if total_inflow_liters > 0 else 0
    return {
        'non_revenue_water_liters': max(0, non_revenue_water),
        'loss_percentage': round(max(0, loss_pct), 2),
        'is_acceptable': loss_pct < 10.0
    }
