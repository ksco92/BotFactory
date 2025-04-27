"""Handler for the Watchdog2 bot."""

import json
import os

from discord.discord_client import DiscordClient
from utils.ddb_client import DdbClient
from utils.sqs_client import SqsClient
from utils.watchdog_2.get_registered_users import get_registered_users
from utils.watchdog_2.raid_alert import raid_alert
from utils.watchdog_2.update_contact_info import update_contact_info


def watchdog2(event: dict, _: dict) -> None:
    """
    Handle a request to Watchdog2.

    :param event: AWS event from SQS.
    :param _: AWS context.
    """
    origination_number = os.environ.get("ORIGINATION_NUMBER")
    discord_client = DiscordClient(os.environ.get("BOT_SECRET_NAME"))
    sqs_queue_url = os.environ.get("SQS_QUEUE_URL")
    contact_info_table_name = os.environ.get("CONTACT_INFO_TABLE_NAME")
    pinpoint_app_id = os.environ.get("PINPOINT_APP_ID")
    sqs_client = SqsClient()
    ddb_client = DdbClient()

    messages = [message for message in event["Records"]]

    for message in messages:
        body = json.loads(message["body"])
        command = body["command"]
        options = body["options"]
        command_issuer = body["command_issuer"]
        channel_id = body["channel_id"]

        if command == "update2":
            try:
                update_contact_info(
                    command_issuer,
                    options[0]["value"],
                    contact_info_table_name,
                )
                discord_client.send_message_to_channel(
                    {
                        "content": "Info updated!",
                    },
                    channel_id,
                )

            except ValueError:
                discord_client.send_message_to_channel(
                    {
                        "content": """
                    [ValueError]: Use this format for your number +12223334455,
                    see this: https://en.wikipedia.org/wiki/E.164
                    """,
                    },
                    channel_id,
                )

            except Exception as e:
                discord_client.send_message_to_channel(
                    {
                        "content": str(e),
                    },
                    channel_id,
                )

        elif command == "raid2":
            try:
                discord_user = discord_client.get_user(options[0]["value"])
                ddb_item = ddb_client.get_item(
                    contact_info_table_name,
                    "discord_user",
                    discord_user,
                )
                phone_number = ddb_item["phone_number"]["S"]  # type: ignore
                raid_alert(pinpoint_app_id, origination_number, phone_number)
                discord_client.send_message_to_channel(
                    {
                        "content": "User has been contacted!",
                    },
                    channel_id,
                )

            except Exception as e:
                discord_client.send_message_to_channel(
                    {
                        "content": str(e),
                    },
                    channel_id,
                )

        elif command == "registered_users2":
            try:
                users = get_registered_users(contact_info_table_name)
                discord_client.send_message_to_channel(
                    {
                        "content": "\n".join([user for user in users]),
                    },
                    channel_id,
                )

            except Exception as e:
                discord_client.send_message_to_channel(
                    {
                        "content": str(e),
                    },
                    channel_id,
                )

        sqs_client.delete_sqs_message(sqs_queue_url, message["receiptHandle"])
