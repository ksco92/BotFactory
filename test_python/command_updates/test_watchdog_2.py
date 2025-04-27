"""Test for the watchdog_2.py command update module."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from command_updates.watchdog_2 import watchdog2_commands


def mock_response(status_code: int) -> MagicMock:
    """
    Create a mock response with the specified HTTP status code.

    :param status_code: HTTP status code for the mock response.
    :return: A MagicMock mimicking a requests.Response object.
    """
    response = MagicMock()
    response.status_code = status_code
    # If status_code >= 400, we simulate requests raising an HTTPError.
    response.raise_for_status.side_effect = (
        None if status_code < 400 else requests.exceptions.HTTPError()
    )
    return response


def test_watchdog2_commands_success() -> None:
    """
    Test that watchdog2_commands registers three commands successfully.

    This test verifies behavior when the HTTP status code is < 400.
    """
    with (
        patch("command_updates.watchdog_2.requests.post") as mock_requests_post,
        patch(
            "command_updates.watchdog_2.SecretsManagerClient",
        ) as mock_secrets_manager_class,
    ):
        # Mock the SecretsManagerClient so it returns fake credentials.
        instance = mock_secrets_manager_class.return_value
        instance.get_secret.return_value = {
            "ApplicationId": "1234567890",
            "Token": "fake-bot-token",
        }

        # Configure the mock for requests.post so all calls return 200.
        mock_requests_post.side_effect = [
            mock_response(200),
            mock_response(200),
            mock_response(200),
        ]

        # Run the function under test
        watchdog2_commands({}, {})

        # Verify exactly 3 POST calls are made
        assert (
            mock_requests_post.call_count == 3
        ), "Expected 3 POST calls for 3 commands."

        # Check that each call had the correct auth header
        for call_args in mock_requests_post.call_args_list:
            _, call_kwargs = call_args
            headers = call_kwargs.get("headers", {})
            assert headers.get("Authorization") == "Bot fake-bot-token"

        # Check that each registered command matches one of update2, registered_users2, raid2
        payloads = [call[1]["json"] for call in mock_requests_post.call_args_list]
        command_names = {p["name"] for p in payloads}
        assert command_names == {
            "update2",
            "registered_users2",
            "raid2",
        }, "Expected the commands to be update2, registered_users2, and raid2."


def test_watchdog2_commands_failure() -> None:
    """
    Test that watchdog2_commands raises an HTTPError.

    This test verifies behavior if any call to requests.post returns a 400+ status code.
    """
    with (
        patch("command_updates.watchdog_2.requests.post") as mock_requests_post,
        patch(
            "command_updates.watchdog_2.SecretsManagerClient",
        ) as mock_secrets_manager_class,
    ):
        instance = mock_secrets_manager_class.return_value
        instance.get_secret.return_value = {
            "ApplicationId": "1234567890",
            "Token": "fake-bot-token",
        }

        # First two succeed, the third fails with a 400-level error
        mock_requests_post.side_effect = [
            mock_response(200),
            mock_response(200),
            mock_response(400),
        ]

        with pytest.raises(requests.exceptions.HTTPError):
            watchdog2_commands({}, {})
