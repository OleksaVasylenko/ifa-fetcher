import pytest

from src.ifa_fetcher.main import search_ingredient


@pytest.mark.parametrize(
    "ingredient, ingredients, expected_result",
    [
        ("hello", ["hello"], ("hello", [])),
        ("hello world", ["hello"], ("", ["hello"])),
        ("hello world", ["hello", "world"], ("", ["hello", "world"])),
        ("hello", ["hello world"], ("", ["hello world"])),
    ],
)
def test_search_ingredient(
    ingredient: str, ingredients: list[str], expected_result: tuple[str, list[str]]
) -> None:
    result = search_ingredient(ingredient, ingredients)
    assert result == expected_result
