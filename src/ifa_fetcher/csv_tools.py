import csv
import sys
from collections import OrderedDict

from .entities import SearchReport


def read_csv(file_path: str) -> dict[str, list[str]]:
    result = OrderedDict()
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row["SKU"], row["Ingredients"])
            ingredients = [i.strip().lower() for i in row["Ingredients"].split(",")]
            result[row["SKU"]] = ingredients

    return result


def write_csv(report: SearchReport, file_path: str) -> None:
    primitive_report = report.as_primitive()
    if not primitive_report:
        raise ValueError("report is empty")

    headers = list(primitive_report[0].keys())
    with open(file_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for item in primitive_report:
            writer.writerow(item)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise systemexit("one arg should be passed")

    read_csv(sys.argv[1])
