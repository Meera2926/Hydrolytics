from src.reports/csv_exporter import generate_csv_report

def test_generates_valid_csv():
    rows = [{'zone': 'Hostel A', 'flow_rate': 30.5, 'status': 'OK'}]
    csv_str = generate_csv_report(rows)
    assert 'Hostel A' in csv_str
    assert '30.5' in csv_str
