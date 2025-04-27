"""Add points to a user in DDB."""

from datetime import datetime
from uuid import uuid4

from utils.ddb_client import DdbClient


def add_points(discord_user: str, points: int, issuer: str) -> None:
    """
    Add points to a user in DDB.

    :param discord_user: Discord user to add points to.
    :param points: Number of points to add.
    :param issuer: Issuer of the user.
    :raises ValueError: If the issuer is the same as the user.
    """
    if discord_user == issuer:
        raise ValueError("You can't do transactions for yourself. Don't be a dick.")

    ddb_client = DdbClient()

    data = {
        "transaction_id": {"S": str(uuid4())},
        "discord_user": {"S": discord_user},
        "points": {"N": str(points)},
        "created_datetime": {"S": datetime.utcnow().isoformat()},
        "issuer": {"S": issuer},
    }

    ddb_client.put_item("points", data)
