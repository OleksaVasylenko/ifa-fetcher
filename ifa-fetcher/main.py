import csv_input
import entities
import fetcher


def search_ingredient(
    ingredient: str, ingredient_sample: list[str]
) -> tuple[str, list[str]]:
    if ingredient in ingredient_sample:
        print("Found exact match:", ingredient)
        return ingredient, []

    print("Trying to find partial match...")
    match = []
    for item in ingredient_sample:
        if ingredient in item:
            match.append(item)
    return "", match


def main() -> None:
    items_to_find = csv_input.read_csv("../files/example_input.csv")
    report = entities.SearchReport()
    for sku, ingredients in items_to_find.items():
        print("checking", sku)
        report_unit = entities.SearchReportUnit(SKU=sku)
        for ingr in ingredients:
            findings = fetcher.search(ingr)
            exact_match, partial_match = search_ingredient(ingr, findings)
            exact_match and report_unit.exact_match.append(exact_match)
            if partial_match:
                report_unit.partial_match[ingr] = partial_match

        report.units.append(report_unit)
    print(report.as_primitive())


if __name__ == "__main__":
    main()
