import pytest


def test_index(client):
    response = client.get('/')
    assert b"USAJOBSmapper" in response.data
    