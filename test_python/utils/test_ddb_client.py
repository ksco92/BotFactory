"""Test the DdbClient class."""

from unittest.mock import patch

import pytest

from test_python.test_utils.mock_api_call import mock_make_api_call
from utils.ddb_client import DdbClient


@pytest.fixture
def ddb_client() -> DdbClient:
    """
    Create a DdbClient fixture.

    :return: A DdbClient instance.
    """
    return DdbClient()


def test_get_item(ddb_client: DdbClient) -> None:
    """
    Test that get_item retrieves the correct item from DynamoDB.

    :param ddb_client: A DdbClient instance.
    """
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        response = ddb_client.get_item("dummy_table", "test_key", "test_value")
        assert response["test_key"]["S"] == "test_value"  # type: ignore


def test_put_item(ddb_client: DdbClient) -> None:
    """
    Test that put_item inserts an item into the table without errors.

    :param ddb_client: A DdbClient instance.
    """
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        ddb_client.put_item("dummy_table", {})


def test_scan(ddb_client: DdbClient) -> None:
    """
    Test that scan retrieves items from the table correctly.

    :param ddb_client: A DdbClient instance.
    """
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        response = ddb_client.scan("dummy_table")
        assert len(response) == 2
        assert response[0]["discord_user"]["S"] == "user_1"
        assert response[1]["discord_user"]["S"] == "user_2"
