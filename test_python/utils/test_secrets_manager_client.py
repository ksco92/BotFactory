"""Test the SQS client."""

from unittest.mock import patch

import pytest

from test_python.test_utils.mock_api_call import mock_make_api_call
from utils.secret_manager_client import SecretsManagerClient


@pytest.fixture
def secrets_manager_client() -> SecretsManagerClient:
    """Create a Secrets Manager client."""
    return SecretsManagerClient()


def test_get_secret(secrets_manager_client: SecretsManagerClient) -> None:
    """
    Test delete_sqs_message function.

    :param secrets_manager_client: A SecretsManagerClient.
    :return: None.
    """
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        response = secrets_manager_client.get_secret("dummy")
        assert "PublicKey" in response
        assert "Token" in response
        assert isinstance(response, dict)
