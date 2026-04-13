def verify_iot_api_key(headers, expected_key='campus-iot-secret-2026'):
    token = headers.get('X-API-KEY')
    return token == expected_key
