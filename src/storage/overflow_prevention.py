class OverflowSafetySwitch:
    def __init__(self, high_cutoff_pct=95.0, low_restart_pct=85.0):
        self.high_cutoff = high_cutoff_pct
        self.low_restart = low_restart_pct
        self.pump_active = True

    def update_level(self, current_pct):
        if current_pct >= self.high_cutoff:
            self.pump_active = False
        elif current_pct <= self.low_restart:
            self.pump_active = True
        return self.pump_active
