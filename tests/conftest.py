import pytest

from bskyflask import create_app


@pytest.fixture
def app():
    """To create the app in testing mode"""

    app = create_app(
        {
            "TESTING": True,
        }
    )

    # Here we would init the db ...abs

    yield app


@pytest.fixture
def client(app):
    """client to run tests"""
    return app.test_client()


# We don't have cli actions
# @pytest.fixture
# def runner(app):
#     """to run the cli methods"""
#     return app.test_cli_runner()
