from contextlib import suppress

from . import entities, fetcher
from .csv_input import read_csv


def search_ingredient(
    ingredient: str, ingredient_sample: list[str]
) -> tuple[str, list[str]]:
    folded_ingredient_sample = [i.casefold() for i in ingredient_sample]
    folded_ingredient = ingredient.casefold()

    with suppress(ValueError):
        idx = folded_ingredient_sample.index(folded_ingredient)
        return ingredient_sample[idx], []

    match = []
    for idx, item in enumerate(folded_ingredient_sample):
        for part in folded_ingredient.split():
            if part in item:
                match.append(ingredient_sample[idx])
                continue
    return "", match


def main() -> None:
    items_to_find = read_csv("../files/example_input.csv")
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
