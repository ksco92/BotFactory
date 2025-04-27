"""Update the commands for SimpBot."""

from utils.run_command_updates import run_command_updates


def simp_bot_commands(_: dict, __: dict) -> None:
    """
    Update the commands for SimpBot.

    :param _: Not used.
    :param __: Not used.
    """
    commands = [
        {
            "name": "taylor",
            "type": 1,
            "description": "Sends a random Taylor Swift song quote.",
        },
        {
            "name": "point_balance",
            "type": 1,
            "description": "Sends the points balance of all users.",
        },
        {
            "name": "add_points",
            "type": 1,
            "description": "Add points to a user.",
            "options": [
                {
                    "name": "user",
                    "type": 6,
                    "required": True,
                    "description": "User to add points to.",
                },
                {
                    "name": "points",
                    "type": 4,
                    "required": True,
                    "description": "Amount of points to add.",
                },
            ],
        },
        {
            "name": "remove_points",
            "type": 1,
            "description": "Remove points from a user.",
            "options": [
                {
                    "name": "user",
                    "type": 6,
                    "required": True,
                    "description": "User to remove points from.",
                },
                {
                    "name": "points",
                    "type": 4,
                    "required": True,
                    "description": "Amount of points to remove.",
                },
            ],
        },
    ]

    run_command_updates(commands)
