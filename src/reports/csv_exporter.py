import csv
import io

def generate_csv_report(data_rows):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['zone', 'flow_rate', 'status'])
    writer.writeheader()
    for row in data_rows:
        writer.writerow(row)
    return output.getvalue()
