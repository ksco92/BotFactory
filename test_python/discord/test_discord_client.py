"""Tests for the Discord client."""

import json
from unittest.mock import MagicMock, patch

import pytest

from discord.discord_client import DiscordClient


def test_init(client: DiscordClient) -> None:
    """
    Test the initialization of the DiscordClient.

    :param client: A Discord client.
    :return: None.
    """
    assert client._api_url == "https://discord.com/api"
    assert isinstance(client._secret, dict)


@patch("requests.post")
def test_send_message_to_channel_success(
    mock_post: dict, client: DiscordClient
) -> None:
    """
    Test sending a message to a channel with a success response.

    :param mock_post: Mock post method.
    :param client: A Discord client.
    :return: None.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response
    result = client.send_message_to_channel("Test message", "123456")

    assert result is True

    mock_post.assert_called_once_with(
        "https://discord.com/api/channels/123456/messages",
        headers=client._headers,
        json="Test message",
    )


@patch("requests.post")
def test_send_message_to_channel_failure(
    mock_post: dict, client: DiscordClient
) -> None:
    """
    Test sending a message to a channel with a failure response.

    :param mock_post: Mock post method.
    :param client: A Discord client.
    :return: None.
    """
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_post.return_value = mock_response

    with pytest.raises(Exception):
        client.send_message_to_channel("Test message", "123456")


def test_get_success_response(client: DiscordClient) -> None:
    """
    Test the get_success_response method for a non-ping scenario.

    :param client: A Discord client.
    :return: None.
    """
    content = "Test message"
    response = client.get_success_response(content)
    expected_response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps(
            {
                "type": client.response_types["CHANNEL_MESSAGE_WITH_SOURCE"],
                "data": {
                    "content": content,
                },
            }
        ),
    }
    assert response == expected_response


def test_get_success_response_ping(client: DiscordClient) -> None:
    """
    Test the get_success_response method for a ping scenario.

    :param client: A Discord client.
    :return: None.
    """
    response = client.get_success_response("", True)

    expected_response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps(
            {
                "type": client.response_types["PONG"],
            }
        ),
    }

    assert response == expected_response


def test_get_unauthorized_response(client: DiscordClient) -> None:
    """
    Test the get_unauthorized_response method.

    :param client: A Discord client.
    :return: None.
    """
    content = "Unauthorized access"
    response = client.get_unauthorized_response(content)

    expected_response = {
        "isBase64Encoded": False,
        "statusCode": 401,
        "body": json.dumps(
            {
                "type": client.response_types["MESSAGE_NO_SOURCE"],
                "data": {
                    "content": f"[UNAUTHORIZED]: {content}",
                },
            }
        ),
    }

    assert response == expected_response


def test_get_error_response(client: DiscordClient) -> None:
    """
    Test the get_error_response method.

    :param client: A Discord client.
    :return: None.
    """
    error_message = "Error occurred"
    response = client.get_error_response(error_message)

    expected_response = {
        "isBase64Encoded": False,
        "statusCode": 500,
        "body": json.dumps(
            {
                "type": client.response_types["MESSAGE_NO_SOURCE"],
                "data": {
                    "content": f"[ERROR]: {error_message}",
                },
            }
        ),
    }

    assert response == expected_response


def test_verify_event_signature_failure(
    lambda_bad_ping_event: dict, client: DiscordClient
) -> None:
    """
    Test the verify_event_signature method for a failed verification scenario.

    :param client: A Discord client.
    :return: None.
    """
    with pytest.raises(Exception):
        client.verify_event_signature(lambda_bad_ping_event)


@patch("requests.get")
def test_get_user_success(mock_get: dict, client: DiscordClient) -> None:
    """
    Test the get_user method for a successful response.

    :param client: A Discord client.
    :return: None.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200

    user_data = {
        "id": "123456",
        "username": "TestUser",
        "discriminator": "0001",
        "avatar": "avatar_url",
    }

    mock_response.content = json.dumps(user_data).encode("utf-8")
    mock_get.return_value = mock_response
    user_details = client.get_user("123456")

    assert user_details == "TestUser#0001"

    mock_get.assert_called_once_with(
        f"{client._api_url}/users/123456", headers=client._headers
    )


@patch("requests.get")
def test_get_user_error(mock_get: dict, client: DiscordClient) -> None:
    """
    Test the get_user method for an error response.

    :param client: A Discord client.
    :return: None.
    """
    mock_response = MagicMock()
    mock_response.status_code = 400
    user_data = {}
    mock_response.content = json.dumps(user_data).encode("utf-8")
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError):
        client.get_user("123456")

    mock_get.assert_called_once_with(
        f"{client._api_url}/users/123456", headers=client._headers
    )


def test_get_event_attributes_ping() -> None:
    """
    Test the get_event_attributes method for a ping event.

    :return: None.
    """
    event = {"body": json.dumps({"type": 1})}
    attributes = DiscordClient.get_event_attributes(event)
    assert attributes == {"is_ping": True}


def test_get_event_attributes_command() -> None:
    """
    Test the get_event_attributes method for a command event.

    :return: None.
    """
    event_body = {
        "type": 2,
        "member": {
            "user": {"username": "TestUser", "discriminator": "0001", "id": "123456789"}
        },
        "channel_id": "987654321",
        "data": {
            "name": "test_command",
            "options": [{"name": "option1", "value": "value1"}],
        },
    }

    event = {"body": json.dumps(event_body)}
    attributes = DiscordClient.get_event_attributes(event)

    expected_attributes = {
        "discord_event": event_body,
        "command": "test_command",
        "options": [{"name": "option1", "value": "value1"}],
        "command_issuer": "TestUser#0001",
        "command_issuer_id": "123456789",
        "channel_id": "987654321",
    }

    assert attributes == expected_attributes
