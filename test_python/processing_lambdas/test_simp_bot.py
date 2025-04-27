"""Test for the SimpBot processing lambda."""

import json
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from processing_lambdas.simp_bot import simp_bot


def _make_sqs_record(
    command: str,
    options: list,
    command_issuer: str,
    channel_id: str,
) -> dict:
    """
    Build an SQS record containing a single command.

    :param command: The command name (e.g., 'add_points').
    :param options: The command options.
    :param command_issuer: The user who issued the command.
    :param channel_id: The Discord channel to send responses to.
    :return: An SQS record dict.
    """
    return {
        "body": json.dumps(
            {
                "command": command,
                "options": options,
                "command_issuer": command_issuer,
                "channel_id": channel_id,
            },
        ),
        "receiptHandle": "dummy_receipt_handle",
    }


@pytest.mark.parametrize(
    "command,options",
    [
        (
            "add_points",
            [{"name": "user", "value": "123456"}, {"name": "points", "value": 50}],
        ),
        (
            "remove_points",
            [{"name": "user", "value": "123456"}, {"name": "points", "value": 50}],
        ),
    ],
)
def test_simp_bot_points_happy_path(command: str, options: list) -> None:
    """
    Test that simp_bot handles add_points/remove_points successfully.

    :param command: The command name to test.
    :param options: Command options for add_points/remove_points.
    """
    event = {
        "Records": [
            _make_sqs_record(
                command=command,
                options=options,
                command_issuer="issuer#1111",
                channel_id="987654",
            ),
        ],
    }

    with (
        patch("processing_lambdas.simp_bot.DiscordClient") as mock_discord_client_class,
        patch("processing_lambdas.simp_bot.SqsClient") as mock_sqs_client_class,
        patch("processing_lambdas.simp_bot.add_points") as mock_add_points,
    ):
        mock_discord_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_discord_client_class.return_value = mock_discord_client
        mock_sqs_client_class.return_value = mock_sqs_client

        mock_discord_client.get_user.return_value = "someUser#9999"
        simp_bot(event, {})

        # Check that we used the correct queue handle
        mock_sqs_client.delete_sqs_message.assert_called_once_with(
            "test_queue",
            "dummy_receipt_handle",
        )
        # For remove_points, we pass the points negative
        if command == "remove_points":
            mock_add_points.assert_called_once_with("someUser#9999", -50, "issuer#1111")
        else:
            mock_add_points.assert_called_once_with("someUser#9999", 50, "issuer#1111")

        # Check we posted a success message
        mock_discord_client.send_message_to_channel.assert_called_once_with(
            {"content": "Transaction completed :eggplant:"},
            "987654",
        )


def test_simp_bot_point_balance_happy_path() -> None:
    """Test that simp_bot handles point_balance successfully."""
    event = {
        "Records": [
            _make_sqs_record(
                command="point_balance",
                options=[],
                command_issuer="issuer#1111",
                channel_id="channel123",
            ),
        ],
    }

    mock_balance = [{"discord_user": "Alice#1234", "total_points": 100}]

    with (
        patch("processing_lambdas.simp_bot.DiscordClient") as mock_discord_client_class,
        patch("processing_lambdas.simp_bot.SqsClient") as mock_sqs_client_class,
        patch("processing_lambdas.simp_bot.get_point_balance") as mock_get_balance,
    ):
        mock_discord_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_discord_client_class.return_value = mock_discord_client
        mock_sqs_client_class.return_value = mock_sqs_client

        mock_get_balance.return_value = mock_balance
        simp_bot(event, {})

        mock_discord_client.send_message_to_channel.assert_called_once()
        sent_message_args, _ = mock_discord_client.send_message_to_channel.call_args
        assert sent_message_args[0]["content"].startswith("```")

        mock_sqs_client.delete_sqs_message.assert_called_once_with(
            "test_queue",
            "dummy_receipt_handle",
        )


def test_simp_bot_add_points_exception() -> None:
    """Test that simp_bot handles exceptions in add_points gracefully."""
    event = {
        "Records": [
            _make_sqs_record(
                command="add_points",
                options=[
                    {"name": "user", "value": "123456"},
                    {"name": "points", "value": 999},
                ],
                command_issuer="issuer#9999",
                channel_id="channelXYZ",
            ),
        ],
    }

    with (
        patch("processing_lambdas.simp_bot.DiscordClient") as mock_discord_client_class,
        patch("processing_lambdas.simp_bot.SqsClient") as mock_sqs_client_class,
        patch("processing_lambdas.simp_bot.add_points") as mock_add_points,
    ):
        mock_discord_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_discord_client_class.return_value = mock_discord_client
        mock_sqs_client_class.return_value = mock_sqs_client

        mock_discord_client.get_user.return_value = "issuer#9999"
        mock_add_points.side_effect = ValueError(
            "You can't do transactions for yourself. Don't be a dick.",
        )

        simp_bot(event, {})

        mock_discord_client.send_message_to_channel.assert_called_once()
        args, _ = mock_discord_client.send_message_to_channel.call_args
        assert "You can't do transactions for yourself" in args[0]["content"]

        mock_sqs_client.delete_sqs_message.assert_called_once_with(
            "test_queue",
            "dummy_receipt_handle",
        )


def test_simp_bot_unknown_command() -> None:
    """Test that an unknown command is ignored (no error thrown)."""
    event = {
        "Records": [
            _make_sqs_record(
                command="unknown_command",
                options=[],
                command_issuer="dummy_user",
                channel_id="dummy_channel",
            ),
        ],
    }

    with (
        patch("processing_lambdas.simp_bot.DiscordClient") as mock_discord_client_class,
        patch("processing_lambdas.simp_bot.SqsClient") as mock_sqs_client_class,
    ):
        mock_discord_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_discord_client_class.return_value = mock_discord_client
        mock_sqs_client_class.return_value = mock_sqs_client

        simp_bot(event, {})

        # We only expect the message to be deleted, no calls to add_points or get_point_balance.
        mock_sqs_client.delete_sqs_message.assert_called_once_with(
            "test_queue",
            "dummy_receipt_handle",
        )
        # Because there's no matching if/elif branch, we do NOT call send_message_to_channel.


@pytest.fixture(autouse=True)
def mock_env() -> Generator:
    """Mock environment variables for all tests."""
    # The code references these for secrets + queue URLs
    with patch.dict(
        "os.environ",
        {"BOT_SECRET_NAME": "test_secret", "SQS_QUEUE_URL": "test_queue"},
    ):
        yield


def test_simp_bot_remove_points_exception() -> None:
    """Test that simp_bot handles exceptions in remove_points gracefully."""
    event = {
        "Records": [
            _make_sqs_record(
                command="remove_points",
                options=[
                    {"name": "user", "value": "123456"},
                    {"name": "points", "value": 999},
                ],
                command_issuer="issuer#8888",
                channel_id="channelXYZ",
            ),
        ],
    }

    with (
        patch("processing_lambdas.simp_bot.DiscordClient") as mock_discord_client_class,
        patch("processing_lambdas.simp_bot.SqsClient") as mock_sqs_client_class,
        patch("processing_lambdas.simp_bot.add_points") as mock_add_points,
    ):
        mock_discord_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_discord_client_class.return_value = mock_discord_client
        mock_sqs_client_class.return_value = mock_sqs_client

        mock_discord_client.get_user.return_value = "someUser#9999"
        mock_add_points.side_effect = RuntimeError(
            "Some random error during remove_points.",
        )

        simp_bot(event, {})

        # We expect an error message to be posted
        mock_discord_client.send_message_to_channel.assert_called_once()
        args, _ = mock_discord_client.send_message_to_channel.call_args
        assert "Some random error during remove_points." in args[0]["content"]

        mock_sqs_client.delete_sqs_message.assert_called_once_with(
            "test_queue",
            "dummy_receipt_handle",
        )


def test_simp_bot_point_balance_exception() -> None:
    """Test that simp_bot handles exceptions in point_balance gracefully."""
    event = {
        "Records": [
            _make_sqs_record(
                command="point_balance",
                options=[],
                command_issuer="issuer#7777",
                channel_id="channelXYZ",
            ),
        ],
    }

    with (
        patch("processing_lambdas.simp_bot.DiscordClient") as mock_discord_client_class,
        patch("processing_lambdas.simp_bot.SqsClient") as mock_sqs_client_class,
        patch("processing_lambdas.simp_bot.get_point_balance") as mock_get_balance,
    ):
        mock_discord_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_discord_client_class.return_value = mock_discord_client
        mock_sqs_client_class.return_value = mock_sqs_client

        mock_get_balance.side_effect = RuntimeError(
            "Something went wrong fetching balances.",
        )

        simp_bot(event, {})

        mock_discord_client.send_message_to_channel.assert_called_once()
        args, _ = mock_discord_client.send_message_to_channel.call_args
        assert "Something went wrong fetching balances." in args[0]["content"]

        mock_sqs_client.delete_sqs_message.assert_called_once_with(
            "test_queue",
            "dummy_receipt_handle",
        )
