"""Client for DDB operations."""

import logging
from typing import Self

import boto3


class DdbClient:
    """Client for DDB operations."""

    def __init__(self: Self) -> None:
        """Create the client."""
        self.ddb = boto3.client("dynamodb")
        logging.info("SM client created...")

    def get_item(
        self: Self,
        table_name: str,
        key_name: str,
        key_value: str,
        key_data_type: str = "S",
    ) -> dict | None:
        """
        Get an item from a table based on a PK value.

        :param table_name: Name of the table to scan.
        :param key_name: Name of the PK column.
        :param key_value: Value to search for.
        :param key_data_type: Data type of the PK.
        :return: The object in the table if it exists.
        """
        logging.info(f"Getting item where {key_name}={key_value} in {table_name}...")
        results = self.ddb.get_item(
            TableName=table_name,
            Key={
                key_name: {
                    key_data_type: key_value,
                },
            },
        )

        return results["Item"] if "Item" in results else None

    def put_item(self: Self, table_name: str, data: dict) -> None:
        """
        Upsert an item to a table.

        :param table_name: Name of the table to upsert to.
        :param data: Dictionary with the data to upsert.
        :return: None.
        """
        logging.info(f"Upserting item to {table_name}...")

        self.ddb.put_item(TableName=table_name, Item=data)

        logging.info("Item upserted...")

    def scan(self: Self, table_name: str, limit: int = 1000) -> list[dict]:
        """
        Get all the items of a table.

        :param table_name: Name of the table to scan.
        :param limit: Limit of items to scan.
        :return: List of items in the table.
        """
        logging.info(f"Scanning {table_name}...")

        response = self.ddb.scan(TableName=table_name, Limit=limit)
        data = response.get("Items")

        while "LastEvaluatedKey" in response:
            response = self.ddb.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            data.extend(response["Items"])

        logging.info(f"There are {len(data)} items in the table!")

        return data
