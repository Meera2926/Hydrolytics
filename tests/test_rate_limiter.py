from src.api/rate_limiter import SimpleRateLimiter

def test_rate_limiter_blocks_excess_calls():
    limiter = SimpleRateLimiter(max_requests=2)
    assert limiter.is_allowed('127.0.0.1') is True
    assert limiter.is_allowed('127.0.0.1') is True
    assert limiter.is_allowed('127.0.0.1') is False
