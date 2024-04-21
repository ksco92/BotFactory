"""Client for SQS operations."""

import logging
from typing import Self

import boto3


class SqsClient:
    """Client for SQS operations."""

    def __init__(self: Self) -> None:
        """Create the client."""
        self.sqs = boto3.client("sqs")
        logging.info("SQS client created...")

    def delete_sqs_message(self: Self, queue_url: str, receipt_handle: str) -> bool:
        """
        Delete an SQS message from a queue.

        :param queue_url: URL of the queue to remove the message from.
        :param receipt_handle: Receipt handle of the message to delete.
        :return: True.
        """
        logging.info(f"Deleting message from {queue_url}...")

        self.sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

        logging.info("Message deleted!")

        return True

    def send_sqs_message(self: Self, queue_url: str, message: str) -> dict:
        """
        Send a message to an SQS queue.

        :param queue_url: URL of the SQS quque where the message will be sent.
        :param message: Message to be sent.
        :return: Response from SQS.
        """
        logging.info(f"Sending message to {queue_url}...")

        response = self.sqs.send_message(QueueUrl=queue_url, MessageBody=message)

        logging.info("Message sent!")

        return response
