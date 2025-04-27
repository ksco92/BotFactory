"""Test the get_registered_users function."""

from unittest.mock import patch

from test_python.test_utils.mock_api_call import mock_make_api_call
from utils.watchdog_2.get_registered_users import get_registered_users


def test_get_registered_users() -> None:
    """Check that get_registered_users returns the correct list of users."""
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        response = get_registered_users("dummy_table")
        assert len(response) == 2
        assert response[0] == "user_1"
        assert response[1] == "user_2"
