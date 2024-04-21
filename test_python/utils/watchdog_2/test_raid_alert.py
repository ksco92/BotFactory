"""Test the raid_alert function."""

from unittest.mock import patch

from test_python.test_utils.mock_api_call import mock_make_api_call
from utils.watchdog_2.raid_alert import raid_alert


def test_raid_alert() -> None:
    """Test the raid_alert function."""
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        assert raid_alert("app+id", "phone_number", "phone_number")
