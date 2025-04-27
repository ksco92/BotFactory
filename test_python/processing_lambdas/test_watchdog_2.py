"""Tests for the Watchdog2 processing lambda."""

import json
from unittest.mock import MagicMock, patch

import pytest

from processing_lambdas.watchdog_2 import watchdog2


def _make_sqs_record(
    command: str,
    options: list,
    command_issuer: str,
    channel_id: str,
) -> dict:
    """
    Build an SQS record containing a single command.

    :param command: The command name (e.g., 'update2').
    :param options: Command options.
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


def test_watchdog2_update2_happy_path() -> None:
    """Test that watchdog2 handles update2 successfully."""
    event = {
        "Records": [
            _make_sqs_record(
                command="update2",
                options=[{"name": "number", "value": "+12223334444"}],
                command_issuer="issuer#0001",
                channel_id="chan123",
            ),
        ],
    }

    with (
        patch("processing_lambdas.watchdog_2.DiscordClient") as mock_discord_class,
        patch("processing_lambdas.watchdog_2.SqsClient") as mock_sqs_class,
        patch("processing_lambdas.watchdog_2.update_contact_info") as mock_update,
    ):
        mock_discord_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_discord_class.return_value = mock_discord_client
        mock_sqs_class.return_value = mock_sqs_client

        watchdog2(event, {})

        mock_update.assert_called_once_with(
            "issuer#0001",
            "+12223334444",
            "contact_info",
        )
        mock_discord_client.send_message_to_channel.assert_called_once_with(
            {"content": "Info updated!"},
            "chan123",
        )
        mock_sqs_client.delete_sqs_message.assert_called_once_with(
            "test_queue",
            "dummy_receipt_handle",
        )


def test_watchdog2_update2_invalid_number() -> None:
    """Test that watchdog2 handles invalid phone number for update2 gracefully."""
    event = {
        "Records": [
            _make_sqs_record(
                command="update2",
                options=[{"name": "number", "value": "invalid_number"}],
                command_issuer="issuer#0001",
                channel_id="chan123",
            ),
        ],
    }

    with (
        patch("processing_lambdas.watchdog_2.DiscordClient") as mock_discord_class,
        patch("processing_lambdas.watchdog_2.SqsClient") as mock_sqs_class,
        patch("processing_lambdas.watchdog_2.update_contact_info") as mock_update,
    ):
        mock_discord_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_discord_class.return_value = mock_discord_client
        mock_sqs_class.return_value = mock_sqs_client

        mock_update.side_effect = ValueError("Invalid phone number!")
        watchdog2(event, {})

        mock_update.assert_called_once_with(
            "issuer#0001",
            "invalid_number",
            "contact_info",
        )
        mock_discord_client.send_message_to_channel.assert_called_once()
        args, _ = mock_discord_client.send_message_to_channel.call_args
        assert "ValueError" in args[0]["content"]
        mock_sqs_client.delete_sqs_message.assert_called_once_with(
            "test_queue",
            "dummy_receipt_handle",
        )


def test_watchdog2_raid2_happy_path() -> None:
    """Test that watchdog2 handles raid2 successfully."""
    event = {
        "Records": [
            _make_sqs_record(
                command="raid2",
                options=[{"name": "user", "value": "123456"}],
                command_issuer="issuer#0002",
                channel_id="chan999",
            ),
        ],
    }

    fake_ddb_item = {"phone_number": {"S": "+15559990000"}}

    with (
        patch("processing_lambdas.watchdog_2.DiscordClient") as mock_discord_class,
        patch("processing_lambdas.watchdog_2.SqsClient") as mock_sqs_class,
        patch("processing_lambdas.watchdog_2.DdbClient") as mock_ddb_class,
        patch("processing_lambdas.watchdog_2.raid_alert") as mock_raid_alert,
    ):
        mock_discord_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_ddb = MagicMock()
        mock_discord_class.return_value = mock_discord_client
        mock_sqs_class.return_value = mock_sqs_client
        mock_ddb_class.return_value = mock_ddb

        mock_discord_client.get_user.return_value = "someUser#7777"
        mock_ddb.get_item.return_value = fake_ddb_item

        watchdog2(event, {})

        mock_raid_alert.assert_called_once_with(
            "test_pinpoint_app_id",
            "+12223334447",
            "+15559990000",
        )
        mock_discord_client.send_message_to_channel.assert_called_once_with(
            {"content": "User has been contacted!"},
            "chan999",
        )
        mock_sqs_client.delete_sqs_message.assert_called_once_with(
            "test_queue",
            "dummy_receipt_handle",
        )


def test_watchdog2_registered_users2_happy_path() -> None:
    """Test that watchdog2 handles registered_users2 successfully."""
    event = {
        "Records": [
            _make_sqs_record(
                command="registered_users2",
                options=[],
                command_issuer="issuer#0002",
                channel_id="chan444",
            ),
        ],
    }

    with (
        patch("processing_lambdas.watchdog_2.DiscordClient") as mock_discord_class,
        patch("processing_lambdas.watchdog_2.SqsClient") as mock_sqs_class,
        patch("processing_lambdas.watchdog_2.get_registered_users") as mock_get_users,
    ):
        mock_discord_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_discord_class.return_value = mock_discord_client
        mock_sqs_class.return_value = mock_sqs_client

        mock_get_users.return_value = ["UserA#1111", "UserB#2222"]
        watchdog2(event, {})

        mock_discord_client.send_message_to_channel.assert_called_once_with(
            {"content": "UserA#1111\nUserB#2222"},
            "chan444",
        )
        mock_sqs_client.delete_sqs_message.assert_called_once_with(
            "test_queue",
            "dummy_receipt_handle",
        )


def test_watchdog2_raid2_exception() -> None:
    """Test that watchdog2 handles an exception in raid2 gracefully."""
    event = {
        "Records": [
            _make_sqs_record(
                command="raid2",
                options=[{"name": "user", "value": "987654"}],
                command_issuer="issuer#0003",
                channel_id="chan321",
            ),
        ],
    }

    with (
        patch("processing_lambdas.watchdog_2.DiscordClient") as mock_discord_class,
        patch("processing_lambdas.watchdog_2.SqsClient") as mock_sqs_class,
        patch("processing_lambdas.watchdog_2.DdbClient") as mock_ddb_class,
    ):
        mock_discord_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_ddb = MagicMock()
        mock_discord_class.return_value = mock_discord_client
        mock_sqs_class.return_value = mock_sqs_client
        mock_ddb_class.return_value = mock_ddb

        mock_discord_client.get_user.side_effect = RuntimeError("Error fetching user!")
        watchdog2(event, {})

        mock_discord_client.send_message_to_channel.assert_called_once()
        args, _ = mock_discord_client.send_message_to_channel.call_args
        assert "Error fetching user!" in args[0]["content"]
        mock_sqs_client.delete_sqs_message.assert_called_once_with(
            "test_queue",
            "dummy_receipt_handle",
        )


@pytest.fixture(autouse=True)
def mock_env() -> None:
    """Mock environment variables for all tests."""
    with patch.dict(
        "os.environ",
        {
            "BOT_SECRET_NAME": "test_secret",
            "SQS_QUEUE_URL": "test_queue",
            "CONTACT_INFO_TABLE_NAME": "contact_info",
            "PINPOINT_APP_ID": "test_pinpoint_app_id",
            "ORIGINATION_NUMBER": "+12223334447",
        },
    ):
        yield


def test_watchdog2_registered_users2_exception() -> None:
    """Test that watchdog2 handles an exception in registered_users2 gracefully."""
    event = {
        "Records": [
            _make_sqs_record(
                command="registered_users2",
                options=[],
                command_issuer="issuer#9999",
                channel_id="chanABC",
            ),
        ],
    }

    with (
        patch("processing_lambdas.watchdog_2.DiscordClient") as mock_discord_class,
        patch("processing_lambdas.watchdog_2.SqsClient") as mock_sqs_class,
        patch("processing_lambdas.watchdog_2.get_registered_users") as mock_get_users,
    ):
        mock_discord_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_discord_class.return_value = mock_discord_client
        mock_sqs_class.return_value = mock_sqs_client

        mock_get_users.side_effect = RuntimeError(
            "Failed to list users for some reason.",
        )

        watchdog2(event, {})

        mock_discord_client.send_message_to_channel.assert_called_once()
        args, _ = mock_discord_client.send_message_to_channel.call_args
        assert "Failed to list users for some reason." in args[0]["content"]

        mock_sqs_client.delete_sqs_message.assert_called_once_with(
            "test_queue",
            "dummy_receipt_handle",
        )


def test_watchdog2_update2_ddb_exception() -> None:
    """Test that watchdog2 handles a generic exception in update2 gracefully."""
    event = {
        "Records": [
            _make_sqs_record(
                command="update2",
                options=[{"name": "number", "value": "+10001112222"}],
                command_issuer="issuer#1000",
                channel_id="chanXYZ",
            ),
        ],
    }

    with (
        patch("processing_lambdas.watchdog_2.DiscordClient") as mock_discord_class,
        patch("processing_lambdas.watchdog_2.SqsClient") as mock_sqs_class,
        patch("processing_lambdas.watchdog_2.update_contact_info") as mock_update_info,
    ):
        mock_discord_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_discord_class.return_value = mock_discord_client
        mock_sqs_class.return_value = mock_sqs_client

        mock_update_info.side_effect = RuntimeError("DynamoDB is down!")

        watchdog2(event, {})

        mock_discord_client.send_message_to_channel.assert_called_once()
        args, _ = mock_discord_client.send_message_to_channel.call_args
        assert "DynamoDB is down!" in args[0]["content"]

        mock_sqs_client.delete_sqs_message.assert_called_once_with(
            "test_queue",
            "dummy_receipt_handle",
        )
