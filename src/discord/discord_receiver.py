"""Handler for discord bot receiver Lambda function."""

import json
import os

from discord.discord_client import DiscordClient
from utils.sqs_client import SqsClient


def discord_receiver(event: dict, _: dict) -> dict:
    """
    Receive an event sent to a discord bot.

    :param event: AWS Lambda event.
    :param _: AWS Lambda context.
    :return: Response to be sent to Discord.
    """
    discord_client = DiscordClient(os.environ.get("BOT_SECRET_NAME"))
    sqs_client = SqsClient()
    sqs_queue_url = os.environ.get("SQS_QUEUE_URL")

    try:
        discord_client.verify_event_signature(event)
    except Exception as e:
        return discord_client.get_unauthorized_response(
            f"Invalid request signature: {e}"
        )

    discord_event_attributes = discord_client.get_event_attributes(event)
    is_ping = discord_event_attributes.get("is_ping")

    if is_ping:
        return discord_client.get_success_response(None, ping=is_ping)

    sqs_client.send_sqs_message(sqs_queue_url, json.dumps(discord_event_attributes))

    return discord_client.get_success_response("Working on it...")
