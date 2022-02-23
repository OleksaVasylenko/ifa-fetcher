import os

from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
