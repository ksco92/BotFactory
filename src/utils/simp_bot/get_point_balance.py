"""Get the point balance of all users."""

from collections import defaultdict

from utils.ddb_client import DdbClient


def get_point_balance() -> list[dict]:
    """
    Get the point balance of all users.

    :return: A list with the balance for each user.
    """
    ddb_client = DdbClient()
    data = ddb_client.scan("points")
    points_aggregation = defaultdict(int)

    for transaction in data:
        discord_user = transaction["discord_user"]["S"]
        points = int(transaction["points"]["N"])
        points_aggregation[discord_user] += points

    return [
        {"discord_user": user, "total_points": points}
        for user, points in points_aggregation.items()
    ]
