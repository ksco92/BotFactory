"""Handler for the SimpBot bot."""

import json
import os

from discord.discord_client import DiscordClient
from utils.simp_bot.add_points import add_points
from utils.simp_bot.get_point_balance import get_point_balance
from utils.sqs_client import SqsClient


def simp_bot(event: dict, _: dict) -> None:
    """
    Handle a request to SimpBot.

    :param event: AWS event from SQS.
    :param _: AWS context.
    """
    discord_client = DiscordClient(os.environ.get("BOT_SECRET_NAME"))
    sqs_queue_url = os.environ.get("SQS_QUEUE_URL")
    sqs_client = SqsClient()

    messages = [message for message in event["Records"]]

    for message in messages:
        body = json.loads(message["body"])
        command = body["command"]
        options = body["options"]
        command_issuer = body["command_issuer"]
        channel_id = body["channel_id"]

        if command == "add_points":
            try:
                discord_user = discord_client.get_user(
                    [i for i in options if i["name"] == "user"][0]["value"],
                )
                points = [i for i in options if i["name"] == "points"][0]["value"]
                add_points(discord_user, points, command_issuer)

                discord_client.send_message_to_channel(
                    {
                        "content": "Transaction completed :eggplant:",
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

        elif command == "remove_points":
            try:
                discord_user = discord_client.get_user(
                    [i for i in options if i["name"] == "user"][0]["value"],
                )
                points = [i for i in options if i["name"] == "points"][0]["value"] * -1
                add_points(discord_user, points, command_issuer)

                discord_client.send_message_to_channel(
                    {
                        "content": "Transaction completed :eggplant:",
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

        elif command == "point_balance":
            try:
                data = get_point_balance()

                discord_client.send_message_to_channel(
                    {"content": f"```\n{json.dumps(data, indent=4)}\n```"},
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
