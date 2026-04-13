from src.api/auth_middleware import verify_iot_api_key

def test_auth_middleware_validation():
    assert verify_iot_api_key({'X-API-KEY': 'campus-iot-secret-2026'}) is True
    assert verify_iot_api_key({'X-API-KEY': 'invalid-token'}) is False
