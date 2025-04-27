"""Update the commands to the latest provided version."""

import os

import requests

from utils.secrets_manager_client import SecretsManagerClient


def run_command_updates(commands: list[dict]) -> None:
    """
    Update the commands to the latest provided version.

    :param commands: List of commands to update and their definition.
    """
    bot_secret_name = os.environ.get("BOT_SECRET_NAME")
    sm_client = SecretsManagerClient()
    secret = sm_client.get_secret(bot_secret_name)
    url = f"https://discord.com/api/v10/applications/{secret['ApplicationId']}/commands"
    headers = {"Authorization": f"Bot {secret['Token']}"}

    for command in commands:
        r = requests.post(url, headers=headers, json=command)
        r.raise_for_status()
