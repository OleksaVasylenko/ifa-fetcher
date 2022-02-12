import pytest

from ifa_fetcher.entities import SearchReport, SearchReportUnit
from ifa_fetcher.fetcher import IFAClient
from ifa_fetcher.service import IFAReportService


class IFAClientStub(IFAClient):
    def search_ingredient(self, _: str) -> list[str]:
        pass


@pytest.fixture
def ifa_report_service() -> IFAReportService:
    return IFAReportService(IFAClientStub(url="http://a.com"))


def test_build_report_unit(ifa_report_service: IFAReportService) -> None:
    result = ifa_report_service.build_report_unit("hello", [])
    assert result == SearchReportUnit(SKU="hello", exact_match=[], partial_match={})


def test_build_report(ifa_report_service: IFAReportService) -> None:
    result = ifa_report_service.build_report({})
    assert result == SearchReport([])
