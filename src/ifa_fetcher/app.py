import os

from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from .views import fetcher, fetcher_view

    app.register_blueprint(fetcher)

    return app
