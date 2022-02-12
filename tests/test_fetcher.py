from unittest.mock import ANY

import pytest

from ifa_fetcher.fetcher import (
    IFA_URL,
    IFAClient,
    IFAClientConfig,
    build_form_data_for_search,
    create_ifa_client,
    extract_search_findings,
    headers,
)

from .conftest import IFAServer


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


def test_extract_search_findings(ifa_aqua_response_html: str) -> None:
    assert extract_search_findings(ifa_aqua_response_html) == [
        "Paraquat",
        "Paraquat dichloride (ISO)",
        "Paraquat dimethylsulfate",
    ]


def test_extract_search_findings_absent(ifa_empty_response_html: str) -> None:
    assert extract_search_findings(ifa_empty_response_html) == []


def test_extract_search_findings_empty_page() -> None:
    assert extract_search_findings("") == []


def test_ifa_client(ifa_server: IFAServer) -> None:
    # can not check form data of the request :(
    # https://github.com/pallets/flask/issues/3448
    client = IFAClient(ifa_server.url)
    client.search_ingredient("something")
    assert len(ifa_server.incoming_requests) == 1
    request, *_ = ifa_server.incoming_requests
    assert request.method == "POST"
    assert request.url == ifa_server.url
    assert dict(request.headers) == {**headers, "Content-Length": ANY, "Host": ANY}


@pytest.mark.parametrize(
    "url, env", [(IFA_URL, None), ("http://a.com", {"IFA_URL": "http://a.com"})]
)
def test_ifa_client_config(url: str, env: dict[str, str] | None) -> None:
    result = IFAClientConfig.from_env(env)
    assert result == IFAClientConfig(url=url)


def test_create_ifa_client() -> None:
    assert type(create_ifa_client()) == IFAClient
