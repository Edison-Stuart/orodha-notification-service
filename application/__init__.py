from flask import Flask, Blueprint
from .namespaces import main_ns, notification_ns
from application.config import configure_namespaces
from application.config.db import get_db_connection

API_VERSION="v1"

def create_base_app() -> Flask:
    """
    Creates and returns a base flask application without a db connection.

    Returns:
        app(Flask): Our main flask app with our api and blueprints linked
    """
    app = Flask(__name__, instance_relative_config=False)
    blueprint = Blueprint("Home", __name__)

    configure_namespaces(blueprint, main_ns, notification_ns)

    app.register_blueprint(blueprint, url_prefix=f"/api/{API_VERSION}")

    return app


def create_app() -> Flask:
    """
    Creates and returns a flask application that has a live db connection.

    Returns:
        app(Flask): Our main flask app that has been connected to our database.
    """
    app = create_base_app()
    get_db_connection()
    return app
