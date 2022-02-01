from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SearchReportUnit:
    SKU: str
    exact_match: list[str] = field(default_factory=list)
    partial_match: dict[str, list[str]] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "SKU": self.SKU,
            "exact": self.exact_match,
            "partial": self.partial_match,
        }


@dataclass(frozen=True)
class SearchReport:
    units: list[SearchReportUnit] = field(default_factory=list)

    def as_primitive(self) -> list[dict[str, Any]]:
        return [u.as_dict() for u in self.units]
