"""Credential class used to perform authenticated interactions with an InvenioRDM instance."""

# pylint: disable=no-member
from httpx import AsyncClient, Client
from pydantic import Field, SecretStr

from prefect.blocks.core import Block


class InvenioRDMCredentials(Block):
    """
    Block used to manage authentication with an InvenioRDM instance. 

    Args:
        base_url (str): The InvenioRDM instance base URL.
        token (str): An InvenioRDM instance access token.
    """

    _block_type_name = "InvenioRDM Credentials"

    base_url: str = Field(
        default=...,
        description="The InvenioRDM instance base URL.",
    )

    token: SecretStr = Field(
        default=..., description="An access token to authenticate with the InvenioRDM instance."
    )

    def get_client(self) -> AsyncClient:
        """
        Creates an InvenioRDM REST AsyncClient.

        Returns:
            AsyncClient: An InvenioRDM REST AsyncClient.
        """

        client = AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.token.get_secret_value()}"},
        )
        return client

    def get_sync_client(self) -> Client:
        """
        Creates an InvenioRDM REST Client.

        Returns:
            Client: An InvenioRDM REST Client.
        """

        client = Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.token.get_secret_value()}"},
        )
        return client
