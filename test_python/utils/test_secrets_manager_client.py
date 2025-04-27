"""Test the SecretsManagerClient class."""

from unittest.mock import patch

import pytest

from test_python.test_utils.mock_api_call import mock_make_api_call
from utils.secrets_manager_client import SecretsManagerClient


@pytest.fixture
def secrets_manager_client() -> SecretsManagerClient:
    """
    Create a SecretsManagerClient fixture.

    :return: A SecretsManagerClient instance.
    """
    return SecretsManagerClient()


def test_get_secret(secrets_manager_client: SecretsManagerClient) -> None:
    """
    Test that get_secret retrieves the specified secret correctly.

    :param secrets_manager_client: A SecretsManagerClient instance.
    """
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        response = secrets_manager_client.get_secret("dummy")
        assert "PublicKey" in response
        assert "Token" in response
        assert isinstance(response, dict)
