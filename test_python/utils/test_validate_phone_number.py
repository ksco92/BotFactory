"""Test the validate_phone_number function."""

from utils.validate_phone_number import validate_phone_number


def test_valid_number() -> None:
    """Test the validate_phone_number function with a valid number."""
    assert validate_phone_number("+12223334444")


def test_invalid_numbers() -> None:
    """Test the validate_phone_number function with an invalid number."""
    assert not validate_phone_number("12223334444")
    assert not validate_phone_number("2223334444")
    assert not validate_phone_number("3334444")
