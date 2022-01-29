from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SearchReport:
    units: list[SearchReportUnit]

    def as_primitive(self) -> list[dict[str, Any]]:
        return [u.as_dict() for u in self.units]


@dataclass(frozen=True)
class SearchReportUnit:
    SKU: str
    exact_match: list[str]
    partial_match: dict[str, list[str]]

    def as_dict(self) -> dict[str, Any]:
        return {
            "SKU": self.SKU,
            "exact": self.exact_match,
            "partial": self.partial_match,
        }
