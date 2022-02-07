import pytest

from ifa_fetcher.fetcher import build_form_data_for_search


def test_build_form_data_for_search() -> None:
    term = "hello"
    assert build_form_data_for_search(term) == {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "Tbox_sub": term,
        "Tbox_cas": "",
        "Butsearch": "Search",
    }


def test_build_form_data_for_search() -> None:
    with pytest.raises(ValueError):
        build_form_data_for_search("")
