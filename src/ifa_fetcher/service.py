from collections import OrderedDict

from .entities import SearchReport, SearchReportUnit
from .fetcher import IFAClient
from .search import search_ingredient


class IFAReportService:
    def __init__(self, ifa_client: IFAClient):
        self._client = ifa_client

    def build_report_unit(self, sku: str, ingredients: list[str]) -> SearchReportUnit:
        result = SearchReportUnit(SKU=sku)
        for ingr in ingredients:
            findings = self._client.search_ingredient(ingr)
            exact_match, partial_match = search_ingredient(ingr, findings)
            exact_match and result.exact_match.append(exact_match)
            if partial_match:
                result.partial_match[ingr] = partial_match
        return result

    def build_report(self, items_to_find: OrderedDict) -> SearchReport:
        result = SearchReport()
        for sku, ingredients in items_to_find.items():
            report_unit = self.build_report_unit(sku, ingredients)
            result.units.append(report_unit)
        return result
