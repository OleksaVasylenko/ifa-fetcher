import os
from collections import OrderedDict
from concurrent.futures import Executor, ThreadPoolExecutor, wait
from dataclasses import dataclass

from .entities import SearchReport, SearchReportUnit
from .fetcher import IFAClient
from .search import search_ingredient


@dataclass(frozen=True)
class IFAReportServiceConfig:
    max_workers: int = 2

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> "IFAReportServiceConfig":
        env = env or os.environ
        return cls(
            max_workers=env.get("IFA_REPORT_MAX_WORKERS") or cls.max_workers,
        )


class IFAReportService:
    def __init__(self, ifa_client: IFAClient, max_workers: int):
        self._client = ifa_client
        self._max_workers = max_workers

    def build_report_unit(self, sku: str, ingredients: list[str]) -> SearchReportUnit:
        result = SearchReportUnit(SKU=sku)
        search_results = self._client.search_ingredients(ingredients)
        for search_result in search_results:
            ingr = search_result.ingredient
            findings = search_result.findings
            exact_match, partial_match = search_ingredient(ingr, findings)
            exact_match and result.exact_match.append(exact_match)
            if partial_match:
                result.partial_match[ingr] = partial_match
        return result

    def build_report(self, items_to_find: OrderedDict) -> SearchReport:
        result = SearchReport()
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            sku_to_fut = OrderedDict({})
            for sku, ingredients in items_to_find.items():
                fut = executor.submit(self.build_report_unit, sku, ingredients)
                sku_to_fut[sku] = fut
            wait(sku_to_fut.values())
            for sku, fut in sku_to_fut.items():
                report_unit = fut.result()
                result.units.append(report_unit)
        return result


def create_ifa_report_service(ifa_client: IFAClient) -> IFAReportService:
    config = IFAReportServiceConfig.from_env()
    return IFAReportService(ifa_client=ifa_client, max_workers=config.max_workers)
