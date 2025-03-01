from datetime import datetime
from typing import NamedTuple

from ._generated_api_client.api import check_authentication, list_api_keys
from ._generated_api_client.client import get_base_url, get_headers, set_headers


class ApiKeyInfo(NamedTuple):
    """
    Named tuple containing information about an API key

    Attributes:
        name: Unique name of the API key
        created_at: When the API key was created
    """

    name: str
    created_at: datetime


class OrcaCredentials:
    """
    Class for managing Orca API credentials
    """

    @staticmethod
    def get_api_url() -> str:
        """
        Get the Orca API base URL that is currently being used
        """
        return get_base_url()

    @staticmethod
    def list_api_keys() -> list[ApiKeyInfo]:
        """
        List all API keys that have been created for your org

        Returns:
            A list of named tuples, with the name and creation date time of the API key
        """
        return [ApiKeyInfo(name=api_key.name, created_at=api_key.created_at) for api_key in list_api_keys()]

    @staticmethod
    def is_authenticated() -> bool:
        """
        Check if you are authenticated to interact with the Orca API

        Returns:
            True if you are authenticated, False otherwise
        """
        try:
            return check_authentication()
        except ValueError as e:
            if "Invalid API key" in str(e):
                return False
            raise e

    @staticmethod
    def set_api_key(api_key: str, check_validity: bool = True):
        """
        Set the API key to use for authenticating with the Orca API

        Note:
            The API key can also be provided by setting the `ORCA_API_KEY` environment variable

        Params:
            api_key: The API key to set
            check_validity: Whether to check if the API key is valid and raise an error otherwise

        Raises:
            ValueError: if the API key is invalid and `check_validity` is True
        """
        set_headers(get_headers() | {"Api-Key": api_key})
        if check_validity:
            check_authentication()
