"""Test the update_contact_info function."""

from unittest.mock import patch

import pytest

from test_python.test_utils.mock_api_call import mock_make_api_call
from utils.watchdog_2.update_contact_info import update_contact_info


def test_update_contact_info() -> None:
    """Test the update_contact_info function."""
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        assert update_contact_info("user", "+12223334444", "dummy_table")


def test_update_contact_info_invalid_number() -> None:
    """Test the update_contact_info function with an invalid phone number."""
    with pytest.raises(ValueError):
        update_contact_info("user", "1234", "dummy_table")
