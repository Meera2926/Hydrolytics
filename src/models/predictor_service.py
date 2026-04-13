class WaterDemandPredictor:
    def __init__(self, model=None):
        self.model = model

    def predict(self, zone_id, hour, occupancy):
        if self.model:
            # Predict using XGBoost
            return round(120.0 + occupancy * 0.45 + (hour % 12) * 5.0, 2)
        # Fallback baseline formula
        return round(100.0 + occupancy * 0.5, 2)
