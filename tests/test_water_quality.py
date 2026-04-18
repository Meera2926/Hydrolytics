from src.utils.water_quality_index import evaluate_water_potability

def test_water_potability_checks():
    res = evaluate_water_potability(ph=7.2, turbidity_ntu=2.1, tds_ppm=280)
    assert res['is_potable'] is True
    assert res['status'] == 'POTABLE'
