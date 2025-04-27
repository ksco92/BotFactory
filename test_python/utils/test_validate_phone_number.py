"""Test the validate_phone_number function."""

from utils.validate_phone_number import validate_phone_number


def test_valid_number() -> None:
    """Test that a properly formatted number returns True."""
    assert validate_phone_number("+12223334444")


def test_invalid_numbers() -> None:
    """Test that improperly formatted numbers return False."""
    assert not validate_phone_number("12223334444")
    assert not validate_phone_number("2223334444")
    assert not validate_phone_number("3334444")
