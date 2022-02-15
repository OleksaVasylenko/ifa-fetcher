from collections import OrderedDict
from concurrent.futures import Executor, ThreadPoolExecutor, wait

from .entities import SearchReport, SearchReportUnit
from .fetcher import IFAClient
from .search import search_ingredient


class IFAReportService:
    def __init__(self, ifa_client: IFAClient):
        self._client = ifa_client
        self._executor = ThreadPoolExecutor()

    def build_report_unit(
        self, sku: str, ingredients: list[str], executor: Executor
    ) -> SearchReportUnit:
        result = SearchReportUnit(SKU=sku)
        ingr_to_fut = OrderedDict({})
        for ingr in ingredients:
            fut = executor.submit(self._client.search_ingredient, ingr)
            ingr_to_fut[ingr] = fut
        wait(ingr_to_fut.values())
        for ingr, fut in ingr_to_fut.items():
            findings = fut.result()
            exact_match, partial_match = search_ingredient(ingr, findings)
            exact_match and result.exact_match.append(exact_match)
            if partial_match:
                result.partial_match[ingr] = partial_match
        return result

    def build_report(self, items_to_find: OrderedDict) -> SearchReport:
        result = SearchReport()
        with self._executor as executor:
            sku_to_fut = OrderedDict({})
            for sku, ingredients in items_to_find.items():
                fut = executor.submit(
                    self.build_report_unit, sku, ingredients, executor
                )
                sku_to_fut[sku] = fut
            wait(sku_to_fut.values())
            for sku, fut in sku_to_fut.items():
                report_unit = fut.result()
                result.units.append(report_unit)
        return result
