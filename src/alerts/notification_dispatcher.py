def format_alert_sms(zone_name, leak_rate_lpm):
    return f"HYDROLYTICS ALERT: Leak of {leak_rate_lpm} L/min detected at {zone_name}. Automated isolation valves notified."
