import csv
from collections import OrderedDict
from pathlib import Path

import pytest

from ifa_fetcher.csv_tools import read_csv


@pytest.fixture
def csv_file_path(tmp_path: Path) -> str:
    result = str(tmp_path / "csv_file")
    with open(result, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["SKU", "Ingredients"])
        writer.writerow(["content", "A, b, C"])
    return result


def test_read_csv(csv_file_path: str) -> None:
    result = read_csv(csv_file_path)
    assert result == OrderedDict({"content": ["A", "b", "C"]})
