import pytest


def test_index(client, auth):
    """
    Test index, both loged in and not
    """
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Next" not in response.data  # no cursor is None

    auth.login()
    response = client.get("/")
    assert b"Log Out" in response.data
    assert b"noesserio.bsky.social" in response.data
    assert b"Reply" in response.data
