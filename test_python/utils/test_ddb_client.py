"""Test the SQS client."""

from unittest.mock import patch

import pytest

from test_python.test_utils.mock_api_call import mock_make_api_call
from utils.ddb_client import DdbClient


@pytest.fixture
def ddb_client() -> DdbClient:
    """Create a SQS client."""
    return DdbClient()


def test_get_item(ddb_client: DdbClient) -> None:
    """
    Test get_item function.

    :param ddb_client: A DdbClient.
    :return: None.
    """
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        response = ddb_client.get_item("dummy_table", "test_key", "test_value")
        assert response["test_key"]["S"] == "test_value"


def test_put_item(ddb_client: DdbClient) -> None:
    """
    Test put_item function.

    :param ddb_client: A DdbClient.
    :return: None.
    """
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        ddb_client.put_item("dummy_table", {})


def test_scan(ddb_client: DdbClient) -> None:
    """
    Test scan function.

    :param ddb_client: A DdbClient.
    :return: None.
    """
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        response = ddb_client.scan("dummy_table")
        assert len(response) == 2
        assert response[0]["discord_user"]["S"] == "user_1"
        assert response[1]["discord_user"]["S"] == "user_2"
