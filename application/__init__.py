from flask import Flask
from .namespaces import api

def create_app() -> Flask:
    """Creates and returns a flask application."""

    app = Flask(__name__, instance_relative_config=False)
    api.init_app(app)

    return app
