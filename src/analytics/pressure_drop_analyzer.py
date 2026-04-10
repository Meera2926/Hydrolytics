def analyze_pressure_drop(inlet_pressure_bar, outlet_pressure_bar, expected_drop=0.3):
    actual_drop = inlet_pressure_bar - outlet_pressure_bar
    is_abnormal = actual_drop > (expected_drop * 2.5)
    return {
        'pressure_drop_bar': round(actual_drop, 2),
        'is_burst_suspected': is_abnormal,
        'recommendation': 'Inspect pipe junction immediately' if is_abnormal else 'Pressure nominal'
    }
