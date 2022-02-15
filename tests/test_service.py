import pytest

from ifa_fetcher.entities import SearchReport, SearchReportUnit
from ifa_fetcher.fetcher import IFAClient, IFAClientConfig, IFASearchResult
from ifa_fetcher.service import (
    IFAReportService,
    IFAReportServiceConfig,
    create_ifa_report_service,
)


class IFAClientStub(IFAClient):
    def search_ingredient(self, ingredient: str) -> IFASearchResult:
        return IFASearchResult(ingredient, ["a", "ab", "c", "d"])


@pytest.fixture
def ifa_client_stub() -> IFAClient:
    return IFAClientStub(url="http://a.com", concurrent_requests=2)


@pytest.fixture
def ifa_report_service_config() -> IFAReportServiceConfig:
    return IFAReportServiceConfig()


@pytest.fixture
def ifa_report_service(
    ifa_report_service_config: IFAReportServiceConfig, ifa_client_stub: IFAClient
) -> IFAReportService:
    max_workers = ifa_report_service_config.max_workers
    return IFAReportService(ifa_client_stub, max_workers)


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


@pytest.mark.parametrize(
    "max_workers, env",
    [
        (2, None),
        (1, {"IFA_REPORT_MAX_WORKERS": 1}),
    ],
)
def test_ifa_report_service_config(
    max_workers: int, env: dict[str, str] | None
) -> None:
    result = IFAReportServiceConfig.from_env(env)
    assert result == IFAReportServiceConfig(max_workers=max_workers)


def test_create_ifa_client(ifa_client_stub: IFAClient) -> None:
    assert type(create_ifa_report_service(ifa_client_stub)) == IFAReportService
