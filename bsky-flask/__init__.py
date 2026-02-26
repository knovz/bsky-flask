import os

from flask import Flask


def create_app(test_config=None):
    """Factory. Create and configure the app."""
    # instance_relative_config means "instance" folder holds local data that should not be commited
    app = Flask(__name__, instance_relative_config=True)
    # Here we can add configuration
    # For example a DATABASE, SECRET_KEY or whatever
    # We will start with no DB

    if test_config is None:
        # Load instance config, if exists
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config passed on
        app.config.from_mapping(test_config)

    # make sure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # If we are using a DB we must init db

    # Test hello page, to check app is running
    @app.route("/hello")
    def hello():
        return "BSKY-FLASK app is running"

    # This is a factory, return the app
    return app
