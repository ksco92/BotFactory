"""Send raid alerts to a user."""

from utils.pinpoint_client import PinpointClient


def raid_alert(
    pinpoint_app_id: str,
    origination_number: str,
    destination_number: str,
) -> bool:
    """
    Send raid alerts to a user.

    :param pinpoint_app_id: Pinpoint application ID.
    :param origination_number: Number to send the alerts from.
    :param destination_number: Number to send the alerts to.
    :return: True.
    """
    pinpoint_client = PinpointClient()
    message = "You are being raided! Shield up!"
    voice_message = f"<speak>{message}</speak>"

    pinpoint_client.send_sms_message(
        pinpoint_app_id,
        origination_number,
        destination_number,
        message,
    )
    pinpoint_client.send_voice_message(
        origination_number,
        destination_number,
        voice_message,
    )

    return True
