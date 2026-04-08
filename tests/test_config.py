from src.config.settings import Config

def test_default_config_values():
    assert Config.DEFAULT_LEAK_THRESHOLD_L_PER_MIN == 25.0
    assert 0 in Config.NIGHT_HOURS
    assert 3 in Config.NIGHT_HOURS
