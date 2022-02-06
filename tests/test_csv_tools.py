import csv
from collections import OrderedDict
from pathlib import Path

import pytest

from ifa_fetcher.csv_tools import read_csv, write_csv
from ifa_fetcher.entities import SearchReport, SearchReportUnit


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


def test_write_csv(tmp_path: Path) -> None:
    unit = SearchReportUnit(SKU="123", exact_match="A", partial_match={"B": ["c", "D"]})
    report = SearchReport([unit])
    path = tmp_path / "output.csv"
    write_csv(report, path)
    with open(path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        assert next(reader) == {
            "SKU": "123",
            "exact": "A",
            "partial": "{'B': ['c', 'D']}",
        }


def test_write_csv_empty_report() -> None:
    report = SearchReport([])
    with pytest.raises(ValueError):
        write_csv(report, "any_path")
