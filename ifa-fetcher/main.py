import csv_input
import entities
import fetcher


def main() -> None:
    items_to_find = csv_input.read_csv("../files/example_input.csv")
    report = entities.SearchReport()
    for sku, ingredients in items_to_find.items():
        print("checking", sku)
        report_unit = entities.SearchReportUnit(SKU=sku)
        for ingr in ingredients:
            findings = fetcher.search(ingr)
            if ingr in findings:
                print("Found exact match:", ingr)
                report_unit.exact_match.append(ingr)
            else:
                print("Trying to find partial match...")
                match = []
                for item in findings:
                    if ingr in item:
                        match.append(item)
                if match:
                    print("Partial match:", ingr, match)
                    report_unit.partial_match[ingr] = match

        report.units.append(report_unit)
    print(report.as_primitive())


if __name__ == "__main__":
    main()
