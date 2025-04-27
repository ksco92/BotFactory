"""Tests for the discord receiver handler."""

import json
import os
from unittest.mock import patch

from discord.discord_client import DiscordClient
from discord.discord_receiver import discord_receiver
from test_python.test_utils.mock_api_call import mock_make_api_call


def mock_verify_event_signature(_: DiscordClient, __: dict) -> bool:
    """
    Mock verify event signature.

    :param _: Discord client.
    :param __: Event data.
    :return: True.
    """
    return True


def test_discord_receiver_bad_ping(
    client: DiscordClient,
    lambda_bad_ping_event: dict,
) -> None:
    """
    Test that a ping with a bad signature returns an error.

    :param client: A Discord client.
    :param lambda_bad_ping_event: Lambda bad ping discord event.
    """
    os.environ["BOT_SECRET_NAME"] = "test_secret"
    os.environ["SQS_QUEUE_URL"] = "test_queue"

    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        response = discord_receiver(lambda_bad_ping_event, {})
        assert response["statusCode"] == 401


def test_discord_receiver_good_ping(
    client: DiscordClient,
    lambda_bad_ping_event: dict,
) -> None:
    """
    Test that a ping with a good signature returns a 200.

    :param client: A Discord client.
    :param lambda_bad_ping_event: Lambda bad ping discord event.
    """
    os.environ["BOT_SECRET_NAME"] = "test_secret"
    os.environ["SQS_QUEUE_URL"] = "test_queue"

    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        with patch(
            "discord.discord_client.DiscordClient.verify_event_signature",
            new=mock_verify_event_signature,
        ):
            response = discord_receiver(lambda_bad_ping_event, {})
            assert response["statusCode"] == 200
            assert json.loads(response["body"]) == {"type": 1}


def test_discord_receiver_forward_to_sqs(
    client: DiscordClient,
    lambda_bad_not_ping_discord_event: dict,
) -> None:
    """
    Test that a discord event gets sent to SQS and returns a success.

    :param client: A Discord client.
    :param lambda_bad_not_ping_discord_event: Lambda discord event.
    """
    os.environ["BOT_SECRET_NAME"] = "test_secret"
    os.environ["SQS_QUEUE_URL"] = "test_queue"

    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        with patch(
            "discord.discord_client.DiscordClient.verify_event_signature",
            new=mock_verify_event_signature,
        ):
            response = discord_receiver(lambda_bad_not_ping_discord_event, {})
            assert response["statusCode"] == 200
            assert json.loads(response["body"]) == {
                "data": {"content": "Working on it..."},
                "type": 4,
            }
