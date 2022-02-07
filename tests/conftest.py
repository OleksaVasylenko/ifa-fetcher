import os
import pathlib

import pytest

tests_dir = pathlib.Path(os.path.dirname(__file__))
files_dir = tests_dir / "files"


@pytest.fixture
def ifa_aqua_response_html() -> str:
    return (files_dir / "aqua_canonical_response.html").read_text()


@pytest.fixture
def ifa_empty_response_html() -> str:
    return (files_dir / "ifa_empty_response.html").read_text()
