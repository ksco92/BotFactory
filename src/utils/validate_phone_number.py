"""Function to validate a phone number."""

import re


def validate_phone_number(phone_number: str) -> bool:
    """
    Validate a phone number looks like: +12223334444.

    :param phone_number: Phone number to validate.
    :return: Whether the number is valid or not.
    """
    pattern = re.compile(r"^\+[0-9]{11}$")
    return bool(re.search(pattern, phone_number))
