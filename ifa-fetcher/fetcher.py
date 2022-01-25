import sys
import urllib.parse
from typing import Any

import requests
from bs4 import BeautifulSoup

url = "https://limitvalue.ifa.dguv.de/WebForm_gw2.aspx"
method = "POST"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://limitvalue.ifa.dguv.de",
    "DNT": "1",
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


def main(arg: Any) -> None:
    data = build_form_data_for_search(arg)
    r = requests.post(url, headers=headers, data=data)
    soup = BeautifulSoup(r.text, "html.parser")
    findings = [i.string for i in soup.find_all("a", class_="internal block")]
    print(findings)
    print(r.status_code)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("One arg should be passed")

    main(sys.argv[1])
