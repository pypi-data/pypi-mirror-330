import logging
from typing import Optional

from slidge import BaseGateway, FormField, global_config
from slixmpp import JID

from .api import get_client_from_registration_form
from .cache import Cache


class Gateway(BaseGateway):
    REGISTRATION_INSTRUCTIONS = (
        "Enter mattermost credentials. Get your MMAUTH_TOKEN on the web interface,"
        " using the dev tools of your browser (it's a cookie)."
    )
    REGISTRATION_FIELDS = [
        FormField(var="url", label="Mattermost server URL", required=True),
        FormField(var="token", label="MMAUTH_TOKEN", required=True),
        FormField(var="basepath", label="Base path", value="/api/v4", required=True),
        FormField(
            var="basepath_ws",
            label="Websocket base path",
            value="/websocket",
            required=True,
        ),
        FormField(
            var="strict_ssl",
            label="Strict SSL verification",
            value="1",
            required=False,
            type="boolean",
        ),
    ]

    ROSTER_GROUP = "Mattermost"

    COMPONENT_NAME = "Mattermost (slidge)"
    COMPONENT_TYPE = "mattermost"

    COMPONENT_AVATAR = (
        "https://play-lh.googleusercontent.com/"
        "aX7JaAPkmnkeThK4kgb_HHlBnswXF0sPyNI8I8LNmEMMo1vDvMx32tCzgPMsyEXXzZRc"
    )

    GROUPS = True

    def __init__(self):
        super().__init__()
        self.cache = Cache(global_config.HOME_DIR / "mm_client_cache_v2.sqlite")
        if not logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.getLogger("httpx").setLevel(logging.WARNING)

    async def validate(
        self, user_jid: JID, registration_form: dict[str, Optional[str]]
    ):
        mm_client = get_client_from_registration_form(registration_form, self.cache)
        try:
            await mm_client.login()
        except Exception as e:
            raise ValueError("Could not authenticate: %s - %s", e, e.args)
        if mm_client.me is None:
            raise ValueError("Could not authenticate")
