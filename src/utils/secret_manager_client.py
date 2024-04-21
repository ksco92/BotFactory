"""Client for Secrets Manager operations."""

import json
import logging
from typing import Self

import boto3


class SecretsManagerClient:
    """Client for Secrets Manager operations."""

    def __init__(self: Self) -> None:
        """Create the client."""
        self.secrets_manager = boto3.client("secretsmanager")
        logging.info("SM client created...")

    def get_secret(self: Self, secret_name: str) -> dict:
        """
        Retrieve a secret from AWS SecretsManager based on the name of the secret.

        :param str secret_name: Name of the secret to retrieve.
        :return: Dictionary with the contents of the secret.
        """
        logging.info(f"Retrieving secret {secret_name}...")

        get_secret_value_response = self.secrets_manager.get_secret_value(
            SecretId=secret_name
        )

        logging.info("Secret retrieved...")

        return json.loads(get_secret_value_response["SecretString"])
