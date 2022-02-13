import sys
import time
from collections import OrderedDict

from .csv_tools import read_csv, write_csv
from .entities import SearchReport, SearchReportUnit
from .fetcher import IFAClient, create_ifa_client
from .search import search_ingredient
from .service import IFAReportService


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Please provide input and output file paths")
    in_file_path = sys.argv[1]
    out_file_path = sys.argv[2]
    items_to_find = read_csv(in_file_path)
    ifa_client = create_ifa_client()
    ifa_search_service = IFAReportService(ifa_client)
    start = time.time()
    report = ifa_search_service.build_report(items_to_find)
    print("report generation took seconds:", time.time() - start)
    write_csv(report, out_file_path)


if __name__ == "__main__":
    main()
