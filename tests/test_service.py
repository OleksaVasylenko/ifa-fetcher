import pytest

from ifa_fetcher.entities import SearchReport, SearchReportUnit
from ifa_fetcher.fetcher import IFAClient, IFASearchResult
from ifa_fetcher.service import IFAReportService


class IFAClientStub(IFAClient):
    def search_ingredient(self, ingredient: str) -> IFASearchResult:
        return IFASearchResult(ingredient, ["a", "ab", "c", "d"])


@pytest.fixture
def ifa_report_service() -> IFAReportService:
    return IFAReportService(IFAClientStub(url="http://a.com", concurrent_requests=2))


def test_build_report_unit_match(ifa_report_service: IFAReportService) -> None:
    result = ifa_report_service.build_report_unit("hello", ["a", "c", "e"])
    assert result == SearchReportUnit(
        SKU="hello", exact_match=["a", "c"], partial_match={"a": ["ab"]}
    )


def test_build_report_unit_nonmatch(ifa_report_service: IFAReportService) -> None:
    result = ifa_report_service.build_report_unit("hello", ["e"])
    assert result == SearchReportUnit(SKU="hello", exact_match=[], partial_match={})


def test_build_report(ifa_report_service: IFAReportService) -> None:
    result = ifa_report_service.build_report({"1": ["c"], "2": ["d"]})
    assert result == SearchReport(
        [SearchReportUnit("1", ["c"], {}), SearchReportUnit("2", ["d"], {})]
    )


def test_build_report_empty(ifa_report_service: IFAReportService) -> None:
    result = ifa_report_service.build_report({})
    assert result == SearchReport([])
