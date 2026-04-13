from src.cache/prediction_cache import PredictionCache

def test_cache_put_and_get():
    c = PredictionCache(max_size=2)
    c.put('k1', 100)
    c.put('k2', 200)
    assert c.get('k1') == 100
    c.put('k3', 300)
    assert c.get('k1') is None
    assert c.get('k3') == 300
