from contextlib import suppress


def search_ingredient(
    ingredient: str, ingredient_sample: list[str]
) -> tuple[str, list[str]]:
    folded_ingredient_sample = [i.casefold() for i in ingredient_sample]
    folded_ingredient = ingredient.casefold()

    with suppress(ValueError):
        idx = folded_ingredient_sample.index(folded_ingredient)
        return ingredient_sample[idx], []

    match = []
    folded_terms = folded_ingredient.split()
    for idx, item in enumerate(folded_ingredient_sample):
        for part in folded_terms:
            if part in item:
                match.append(ingredient_sample[idx])
                continue
    return "", match
