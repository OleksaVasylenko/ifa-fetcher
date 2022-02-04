import csv
import sys
from collections import OrderedDict


def read_csv(file_path: str) -> dict[str, list[str]]:
    result = OrderedDict()
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row["SKU"], row["Ingredients"])
            ingredients = [i.strip().lower() for i in row["Ingredients"].split(",")]
            result[row["SKU"]] = ingredients

    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise systemexit("one arg should be passed")

    read_csv(sys.argv[1])
