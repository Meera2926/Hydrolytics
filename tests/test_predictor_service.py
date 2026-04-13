from src.models/predictor_service import WaterDemandPredictor

def test_predictor_service_returns_demand():
    service = WaterDemandPredictor()
    demand = service.predict(zone_id='HOSTEL_A', hour=14, occupancy=200)
    assert demand > 0
    assert isinstance(demand, float)
