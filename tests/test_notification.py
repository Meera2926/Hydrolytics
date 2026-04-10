from src.alerts/notification_dispatcher import format_alert_sms

def test_formats_alert_sms():
    msg = format_alert_sms('Dining Hall', 35.5)
    assert '35.5 L/min' in msg
    assert 'Dining Hall' in msg
