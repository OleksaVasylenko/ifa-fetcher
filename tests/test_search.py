import pytest

from src.ifa_fetcher.main import search_ingredient


def test_search_ingredient_exact() -> None:
    result = search_ingredient("hello", ["hello"])
    assert result == ("hello", [])


def test_search_ingredient_partial_left() -> None:
    result = search_ingredient("hello world", ["hello"])
    assert result == ("", ["hello"])


def test_search_ingredient_partial_right() -> None:
    result = search_ingredient("hello", ["hello world"])
    assert result == ("", ["hello world"])
