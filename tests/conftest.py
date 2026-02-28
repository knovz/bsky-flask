import pytest
import os
from dotenv import load_dotenv

load_dotenv()


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


class AuthActions(object):
    """
    Class to manage login and logout,
    as we will probably need it in several places
    """

    def __init__(self, client):
        self._client = client
        self._bsky_handle = os.getenv("BSKY_HANDLE", "test")
        self._bsky_app_pass = os.getenv("BSKY_APP_PASS", "test")

    def login(self, username=None, password=None):
        """
        Login as username and password.
        If values are empty, env values are used

        Keyword Arguments:
            username {str} -- bsky username
            password {str} -- bsky password
        """
        if username is None:
            username = self._bsky_handle
        if password is None:
            password = self._bsky_app_pass

        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        """logout"""
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    """With this we can call auth.login and auth.logout in a test"""
    return AuthActions(client)
