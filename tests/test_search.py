import pytest

from ifa_fetcher.search import search_ingredient


@pytest.mark.parametrize(
    "ingredient, ingredients, expected_result",
    [
        ("hello", ["hello"], ("hello", [])),
        ("hello world", ["hello"], ("", ["hello"])),
        ("Hello world", ["hello"], ("", ["hello"])),
        ("hello world", ["Hello"], ("", ["Hello"])),
        ("hello world", ["hello", "world"], ("", ["hello", "world"])),
        ("hello world", ["hello", "World"], ("", ["hello", "World"])),
        ("hello", ["hello world"], ("", ["hello world"])),
        ("Hello", ["hello"], ("hello", [])),
        ("hello", ["Hello"], ("Hello", [])),
        ("a", ["a", "ab"], ("a", ["ab"])),
    ],
)
def test_search_ingredient(
    ingredient: str, ingredients: list[str], expected_result: tuple[str, list[str]]
) -> None:
    result = search_ingredient(ingredient, ingredients)
    assert result == expected_result
