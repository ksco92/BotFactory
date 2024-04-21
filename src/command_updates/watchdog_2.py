"""Update the commands for Watchdog2."""

import os

import requests

from utils.get_secret import get_secret


def watchdog2_commands(_: dict, __: dict) -> None:
    """
    Update the commands for Watchdog2.

    :param _: AWS event from SQS.
    :param __: AWS context.
    :return: None.
    """
    bot_secret_name = os.environ.get("BOT_SECRET_NAME")
    secret = get_secret(bot_secret_name)

    url = f"https://discord.com/api/v10/applications/{secret['ApplicationId']}/commands"

    headers = {"Authorization": f"Bot {secret['Token']}"}

    # This is an example CHAT_INPUT or Slash Command, with a type of 1
    update_json = {
        "name": "update2",
        "type": 1,
        "description": "Update your contact information.",
        "options": [
            {
                "name": "number",
                "type": 3,
                "required": True,
                "description": "Your phone number in format +12223334444.",
            },
        ],
    }

    r = requests.post(url, headers=headers, json=update_json)
    r.raise_for_status()

    registered_users_json = {
        "name": "registered_users2",
        "type": 1,
        "description": "Lists all the users registered in Watchdog.",
    }

    r = requests.post(url, headers=headers, json=registered_users_json)
    r.raise_for_status()

    raid_json = {
        "name": "raid2",
        "type": 1,
        "description": "Send a raid alert.",
        "options": [
            {
                "name": "user",
                "type": 6,
                "required": True,
                "description": "User getting raided.",
            },
        ],
    }

    r = requests.post(url, headers=headers, json=raid_json)
    r.raise_for_status()
