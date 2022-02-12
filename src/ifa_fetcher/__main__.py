import sys
from collections import OrderedDict

from . import entities, fetcher
from .csv_tools import read_csv, write_csv
from .search import search_ingredient


class IFASearchService:
    pass

    def build_search_report(self, items_to_find: OrderedDict) -> entities.SearchReport:
        result = entities.SearchReport()
        for sku, ingredients in items_to_find.items():
            report_unit = entities.SearchReportUnit(SKU=sku)
            for ingr in ingredients:
                findings = fetcher.search(ingr)
                exact_match, partial_match = search_ingredient(ingr, findings)
                exact_match and report_unit.exact_match.append(exact_match)
                if partial_match:
                    report_unit.partial_match[ingr] = partial_match

            result.units.append(report_unit)
        return result


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Please provide input and output file paths")
    in_file_path = sys.argv[1]
    out_file_path = sys.argv[2]
    items_to_find = read_csv(in_file_path)
    ifa_search_service = IFASearchService()
    report = ifa_search_service.build_search_report(items_to_find)
    write_csv(report, out_file_path)


if __name__ == "__main__":
    main()
