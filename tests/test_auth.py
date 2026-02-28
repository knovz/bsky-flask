import pytest
from flask import session


def test_login(client, auth):
    assert client.get("/auth/login").status_code == 200


def test_logout(client, auth):
    """login and test logout"""
    auth.login()

    with client:
        auth.logout()
        assert "user" not in session
        assert "bsky" not in session
