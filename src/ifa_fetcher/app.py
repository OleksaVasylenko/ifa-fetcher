import os

from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from .views import fetcher, fetcher_view

    app.register_blueprint(fetcher)
    app.add_url_rule("/", view_func=fetcher_view)

    return app
