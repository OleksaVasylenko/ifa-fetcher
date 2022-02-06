import csv

from .entities import SearchReport


def write_csv(report: SearchReport) -> None:
    primitive_report = report.as_primitive()
    if not primitive_report:
        raise ValueError("report is empty")

    headers = list(primitive_report[0].keys())
    with open("output.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for item in primitive_report:
            writer.writerow(item)
