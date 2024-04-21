"""Client for Pinpoint operations."""

import logging
from typing import Self

import boto3


class PinpointClient:
    """Client for Pinpoint operations."""

    def __init__(self: Self) -> None:
        """Create the client."""
        self.pinpoint = boto3.client("pinpoint")
        self.pinpoint_sms = boto3.client("pinpoint-sms-voice")
        logging.info("Pinpoint client created...")

    def send_sms_message(
        self: Self,
        pinpoint_app_id: str,
        origination_number: str,
        destination_number: str,
        message: str,
    ) -> bool:
        """
        Send SMS message with Pinpoint.

        :param pinpoint_app_id: Pinpoint application ID.
        :param origination_number: Number where the message will be sent from.
        :param destination_number: Number to send the message to.
        :param message: Message to send.
        :return: True.
        """
        logging.info(f"Sending SMS message to {destination_number}...")

        r = self.pinpoint.send_messages(
            ApplicationId=pinpoint_app_id,
            MessageRequest={
                "Addresses": {
                    destination_number: {
                        "ChannelType": "SMS",
                    },
                },
                "MessageConfiguration": {
                    "SMSMessage": {
                        "Body": message,
                        "MessageType": "TRANSACTIONAL",
                        "OriginationNumber": origination_number,
                    }
                },
            },
        )
        print(r)

        logging.info("Message sent!")

        return True

    def send_voice_message(
        self: Self, origination_number: str, destination_number: str, ssml_message: str
    ) -> bool:
        """
        Send a voice message with Pinpoint.

        :param origination_number: Number where the message will be sent from.
        :param destination_number: Number to send the message to.
        :param ssml_message: Message to send.
        :return: True.
        """
        logging.info(f"Sending voice message to {destination_number}...")

        self.pinpoint_sms.send_voice_message(
            DestinationPhoneNumber=destination_number,
            OriginationPhoneNumber=origination_number,
            Content={
                "SSMLMessage": {
                    "LanguageCode": "en-US",
                    "VoiceId": "Matthew",
                    "Text": ssml_message,
                }
            },
        )

        logging.info("Message sent!")

        return True
