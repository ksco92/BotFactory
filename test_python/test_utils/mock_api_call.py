"""Mock boto3 calls."""

import json
import secrets
from typing import Any


def mock_make_api_call(_: Any, operation_name: str, operation_params: dict) -> dict:
    """
    Mock boto3 calls.

    :param _: Unused.
    :param operation_name: Name of the API call.
    :param operation_params: Dictionary with the parameters of the request.
    :raises RuntimeError: If the API call is not implemented.
    :return: The mock API response.
    """
    if operation_name == "GetSecretValue":
        return {
            "SecretString": json.dumps(
                {
                    "PublicKey": secrets.token_hex(32),
                    "Token": "abcd",
                },
            ),
        }
    elif operation_name == "SendMessage":
        return {
            "MessageId": "swrgtsrgfvwr",
        }
    elif operation_name == "DeleteMessage":
        return {}
    elif operation_name == "GetItem":
        return {
            "Item": {
                "test_key": {
                    "S": "test_value",
                },
            },
        }
    elif operation_name == "PutItem":
        return {}
    elif operation_name == "Scan" and "ExclusiveStartKey" not in operation_params:
        return {
            "Items": [
                {
                    "discord_user": {
                        "S": "user_1",
                    },
                },
            ],
            "LastEvaluatedKey": {
                "discord_user": {
                    "S": "user_1",
                },
            },
        }
    elif operation_name == "Scan" and "ExclusiveStartKey" in operation_params:
        return {
            "Items": [
                {
                    "discord_user": {
                        "S": "user_2",
                    },
                },
            ],
        }
    elif operation_name == "SendMessages":
        return {}
    elif operation_name == "SendVoiceMessage":
        return {}

    raise RuntimeError("Mock not implemented")
