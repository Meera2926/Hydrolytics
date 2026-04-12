def calculate_lpcd(total_daily_liters, student_population):
    if student_population <= 0: return 0.0
    lpcd = total_daily_liters / student_population
    # Indian standard for hostels with flushing: 135 LPCD
    return {
        'lpcd': round(lpcd, 1),
        'is_compliant': lpcd <= 135.0,
        'standard_lpcd': 135.0
    }
