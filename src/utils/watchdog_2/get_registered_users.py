"""Get the registered users from DDB."""

import logging

from utils.ddb_client import DdbClient


def get_registered_users(contact_info_table_name: str) -> list[str]:
    """
    Get the registered users from DDB.

    :param contact_info_table_name: The name of the contact info table.
    :return: The list of registered users.
    """
    logging.info("Getting registered users...")

    ddb_client = DdbClient()
    data = ddb_client.scan(contact_info_table_name)

    logging.info(f"There are {len(data)} users!")

    return [user["discord_user"]["S"] for user in data]
