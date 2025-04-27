"""Test the PinpointClient class."""

from unittest.mock import patch

import pytest

from test_python.test_utils.mock_api_call import mock_make_api_call
from utils.pinpoint_client import PinpointClient


@pytest.fixture
def pinpoint_client() -> PinpointClient:
    """
    Create a PinpointClient fixture.

    :return: A PinpointClient instance.
    """
    return PinpointClient()


def test_send_sms_message(pinpoint_client: PinpointClient) -> None:
    """
    Test that send_sms_message returns True without errors.

    :param pinpoint_client: A PinpointClient instance.
    """
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        assert pinpoint_client.send_sms_message(
            "app_id",
            "phone_number",
            "phone_number",
            "message",
        )


def test_send_voice_message(pinpoint_client: PinpointClient) -> None:
    """
    Test that send_voice_message returns True without errors.

    :param pinpoint_client: A PinpointClient instance.
    """
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        assert pinpoint_client.send_voice_message(
            "phone_number",
            "phone_number",
            "message",
        )
