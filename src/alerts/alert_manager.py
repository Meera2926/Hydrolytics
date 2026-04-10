class AlertManager:
    def __init__(self):
        self.active_alerts = []

    def trigger_alert(self, alert_type, zone, description, severity='WARNING'):
        alert = {
            'id': len(self.active_alerts) + 1,
            'type': alert_type,
            'zone': zone,
            'description': description,
            'severity': severity,
            'status': 'OPEN'
        }
        self.active_alerts.append(alert)
        return alert

    def resolve_alert(self, alert_id):
        for a in self.active_alerts:
            if a['id'] == alert_id:
                a['status'] = 'RESOLVED'
                return True
        return False
