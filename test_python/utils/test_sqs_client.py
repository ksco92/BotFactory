"""Test the SQS client."""

from unittest.mock import patch

import pytest

from test_python.test_utils.mock_api_call import mock_make_api_call
from utils.sqs_client import SqsClient


@pytest.fixture
def sqs_client() -> SqsClient:
    """Create a SQS client."""
    return SqsClient()


def test_delete_sqs_message(sqs_client: SqsClient) -> None:
    """
    Test delete_sqs_message function.

    :param sqs_client: An SqsClient.
    :return: None.
    """
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        response = sqs_client.delete_sqs_message("abcd", "abcd")
        assert response


def test_send_sqs_message(sqs_client: SqsClient) -> None:
    """
    Test send_sqs_message function.

    :param sqs_client: An SqsClient.
    :return: None.
    """
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        response = sqs_client.send_sqs_message("abcd", "abcd")
        assert response["MessageId"] == "swrgtsrgfvwr"
