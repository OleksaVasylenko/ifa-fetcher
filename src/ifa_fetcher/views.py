from flask import Blueprint, render_template, request
from flask.typing import ResponseReturnValue

fetcher = Blueprint("fetcher", __name__)


@fetcher.route("/fetcher", methods=("GET", "POST"))
def fetcher_view() -> ResponseReturnValue:
    if request.method == "POST":
        print(request.files)
    return render_template("fetcher/fetcher.html")
