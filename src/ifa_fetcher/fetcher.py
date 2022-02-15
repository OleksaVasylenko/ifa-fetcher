import os
import sys
import urllib.parse
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, wait
from dataclasses import dataclass
from typing import Any

import requests
from bs4 import BeautifulSoup

IFA_URL = "https://limitvalue.ifa.dguv.de/WebForm_gw2.aspx"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://limitvalue.ifa.dguv.de",
    "Dnt": "1",
    "Connection": "keep-alive",
    "Referer": "https://limitvalue.ifa.dguv.de/WebForm_gw2.aspx",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
}

raw_data = {
    "__EVENTTARGET": "",
    "__EVENTARGUMENT": "",
    "Tbox_sub": "",
    "Tbox_cas": "",
    "Butsearch": "Search",
}


def build_form_data_for_search(term: str) -> dict[str, Any]:
    if not term:
        raise ValueError("search term can not be empty")

    result = raw_data.copy()
    result["Tbox_sub"] = urllib.parse.quote_plus(term)
    return result


def extract_search_findings(page_text: str) -> list[str]:
    soup = BeautifulSoup(page_text, "html.parser")
    return [i.string for i in soup.find_all("a", class_="internal block")]


@dataclass(frozen=True)
class IFAClientConfig:
    url: str = IFA_URL
    concurrent_requests: int = 8

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> "IFAClientConfig":
        env = env or os.environ
        return cls(
            url=env.get("IFA_URL") or cls.url,
            concurrent_requests=env.get("IFA_CONCURRENT_REQUESTS")
            or cls.concurrent_requests,
        )


@dataclass(frozen=True)
class IFASearchResult:
    ingredient: str
    findings: list[str]


class IFAClient:
    def __init__(self, url: str):
        self._url = url

    def search_ingredient(self, ingredient: str) -> IFASearchResult:
        data = build_form_data_for_search(ingredient)
        response = requests.post(self._url, headers=headers, data=data)
        findings = extract_search_findings(response.text)
        return IFASearchResult(ingredient=ingredient, findings=findings)

    def search_ingredients(self, ingredients: list[str]) -> list[IFASearchResult]:
        with ThreadPoolExecutor() as executor:
            job = self.search_ingredient
            ingr_to_fut = {i: executor.submit(job, i) for i in ingredients}
            wait(ingr_to_fut.values())
            result = []
            for ingredient in ingredients:
                fut = ingr_to_fut[ingredient]
                search_result = fut.result()
                result.append(search_result)
            return result


def create_ifa_client() -> IFAClient:
    config = IFAClientConfig.from_env()
    client = IFAClient(url=config.url)
    return client
