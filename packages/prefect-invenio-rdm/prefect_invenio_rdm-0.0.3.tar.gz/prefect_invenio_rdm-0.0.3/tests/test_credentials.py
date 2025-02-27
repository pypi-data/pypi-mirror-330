"""Tests credentials.py."""

from httpx import AsyncClient, Client
from prefect_invenio_rdm.credentials import InvenioRDMCredentials


def test_credentials_get_client():
    """Tests that get_client() returns an asynchronous REST client"""
    client = InvenioRDMCredentials(base_url="base_url", token="token_value").get_client()
    assert isinstance(client, AsyncClient)
    assert client.headers["authorization"] == "Bearer token_value"
    assert client.base_url == "base_url/"


def test_credentials_get_sync_client():
    """Tests that get_sync_client() returns a synchronous REST client"""
    client = InvenioRDMCredentials(
        base_url="base_url", token="token_value"
    ).get_sync_client()
    assert isinstance(client, Client)
    assert client.headers["authorization"] == "Bearer token_value"
    assert client.base_url == "base_url/"
