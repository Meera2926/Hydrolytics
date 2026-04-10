from src.alerts/alert_manager import AlertManager

def test_alert_manager_lifecycle():
    mgr = AlertManager()
    alert = mgr.trigger_alert('BURST', 'Hostel A', 'Rapid pressure loss')
    assert alert['id'] == 1
    assert alert['status'] == 'OPEN'
    assert mgr.resolve_alert(1) is True
    assert mgr.active_alerts[0]['status'] == 'RESOLVED'
