from flask import Blueprint
from flask.typing import ResponseReturnValue

fetcher = Blueprint("fetcher", __name__)


@fetcher.route("/fetcher", methods=("GET", "POST"))
def fetcher_view() -> ResponseReturnValue:
    return "OK"
