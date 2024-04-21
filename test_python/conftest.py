"""Shared test configurations."""

from unittest.mock import patch

import pytest

from discord.discord_client import DiscordClient
from test_python.test_utils.mock_api_call import mock_make_api_call


@pytest.fixture
def lambda_bad_ping_event() -> dict:
    """Bad ping event from Lambda."""
    return {
        "headers": {
            "x-signature-ed25519": "3e3bbdfadb48a300f0269f27ef24039aa1a0dc098666abb51f5c72d1a4631da1b0c12444e653c1389a7cc0cd94b4dfbaa178778d9e08773c641c4f875112f508",  # noqa: E501
            "x-signature-timestamp": "1659895662",
        },
        "body": '{"application_id":"1000522198345330799","id":"1005900057511465102","token":"aW50ZXJhY3Rpb246MTAwNTkwMDA1NzUxMTQ2NTEwMjpVZjl2SjhCa1lNQ2NFQ3VDWm5YcU5uZmJxajV6UGZTbmZBYnF0U3lOSlZSS3IxMFU2djd4VlVIeHVEWDBpMWszU2hMQXZ4Uzc2d2RzZ1Q3RFd1N3ZWV1ZRaGlFNkZtbkFBREtXY2RBUnRTSWFjdlFnU1R1bVNtc3p2YUJ1WUdoZQ","type":1,"user":{"avatar":"f049766651539543997b17b413b7d084","avatar_decoration":null,"discriminator":"3832","id":"358434326129541121","public_flags":0,"username":"ksco92"},"version":1}',  # noqa: E501
    }


@pytest.fixture
def lambda_bad_not_ping_discord_event() -> dict:
    """Bad non-ping event from Lambda."""
    return {
        "body": '{"app_permissions":"562949953421311","application_id":"1216559048451952710","channel":{"flags":0,"guild_id":"536204621765672974","icon_emoji":{"id":null,"name":"👀"},"id":"1000523254928257125","last_message_id":"1218954905956384870","name":"watchdog","nsfw":false,"parent_id":"999795158344282202","permissions":"562949953421311","position":66,"rate_limit_per_user":0,"theme_color":null,"topic":null,"type":0},"channel_id":"1000523254928257125","data":{"id":"1218007189893939240","name":"update2","options":[{"name":"number","type":3,"value":"+12068903991"}],"type":1},"entitlement_sku_ids":[],"entitlements":[],"guild":{"features":["INVITE_SPLASH","CHANNEL_ICON_EMOJIS_GENERATED","ANIMATED_ICON","THREE_DAY_THREAD_ARCHIVE"],"id":"536204621765672974","locale":"en-US"},"guild_id":"536204621765672974","guild_locale":"en-US","id":"1219046254009651331","locale":"en-US","member":{"avatar":null,"communication_disabled_until":null,"deaf":false,"flags":0,"joined_at":"2021-01-31T19:16:51.315000+00:00","mute":false,"nick":"CaptSisko1a1","pending":false,"permissions":"562949953421311","premium_since":null,"roles":["536208371569655808","536936167963099137","536205130077569034","999796186376577105","1035736534734880818","966130876184412251","1020845822885253151"],"unusual_dm_activity_until":null,"user":{"avatar":"f049766651539543997b17b413b7d084","avatar_decoration_data":null,"discriminator":"0","global_name":"ksco92","id":"358434326129541121","public_flags":0,"username":"ksco92"}},"token":"","type":2,"version":1}',  # noqa: E501
    }


@pytest.fixture
def client() -> DiscordClient:
    """
    Initialize the DiscordClient with a mock secret name.

    :return: A Discord client.
    """
    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        return DiscordClient("mock_secret_name")
