"""Test for the simp_bot.py command update module."""

from unittest.mock import patch

import pytest

from command_updates.simp_bot import simp_bot_commands


@pytest.mark.parametrize(
    "dummy_event,dummy_context",
    [({}, {}), ({"foo": "bar"}, {"baz": True})],
)
def test_simp_bot_commands_happy_path(dummy_event: dict, dummy_context: dict) -> None:
    """
    Test that simp_bot_commands calls run_command_updates with the expected commands.

    :param dummy_event: An example AWS event dictionary.
    :param dummy_context: An example AWS context dictionary.
    """
    with patch(
        "command_updates.simp_bot.run_command_updates",
    ) as mock_run_command_updates:
        simp_bot_commands(dummy_event, dummy_context)

        # Check that run_command_updates was called exactly once
        assert mock_run_command_updates.call_count == 1

        # Extract the arguments it was called with
        (commands_arg,), _ = mock_run_command_updates.call_args

        # Ensure each command in the list has the expected shape
        assert len(commands_arg) == 4, "Should have exactly 4 commands for SimpBot."
        assert {
            "name": "taylor",
            "type": 1,
            "description": "Sends a random Taylor Swift song quote.",
        } in commands_arg
        assert {
            "name": "point_balance",
            "type": 1,
            "description": "Sends the points balance of all users.",
        } in commands_arg
