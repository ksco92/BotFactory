"""Update the contact info in DDB for a user."""

from utils.ddb_client import DdbClient
from utils.validate_phone_number import validate_phone_number


def update_contact_info(discord_user: str, phone_number: str, table_name: str) -> bool:
    """
    Add or update the number of a user in DDB.

    :param discord_user: User to update the info for.
    :param phone_number: Number to add.
    :param table_name: Name of the DDB table with the contact info.
    :return: True.
    """
    if not validate_phone_number(phone_number):
        raise ValueError("Invalid phone number!")

    dynamo_db_client = DdbClient()

    data = {
        "discord_user": {"S": discord_user},
        "phone_number": {"S": phone_number},
    }

    dynamo_db_client.put_item(table_name, data)

    return True
