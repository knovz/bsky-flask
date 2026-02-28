import pytest
from flask import session


def test_login(client, auth):
    """
    GET returns user form
    POST (via auth) redirects to index and stores user and bsky in session
    """

    assert client.get("/auth/login").status_code == 200

    # login with no params reads user and pass from environment

    with client:
        response = auth.login()
        assert response.headers["Location"] == "/"
        assert "user" in session
        assert "bsky" in session


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("sdsad", "jjdsj", b"Login error"),
        ("noesserio.bsky.social", "jjdsj", b"Login error"),
    ),
)
def test_login_validate_input(auth, username, password, message):
    """login wrong options"""
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    """login and test logout"""
    auth.login()

    with client:
        auth.logout()
        assert "user" not in session
        assert "bsky" not in session
