import asyncio
import logging
from typing import Optional

from slidge import BaseGateway, GatewayUser
from slidge.command.register import FormField, RegistrationType
from slixmpp import JID
from slixmpp.exceptions import XMPPError

from .client import CredentialsValidation
from .types import ChannelId


class Gateway(BaseGateway):
    REGISTRATION_INSTRUCTIONS = "Enter steam credentials"
    REGISTRATION_FIELDS = [
        FormField(var="username", label="Steam username", required=True),
        FormField(var="password", label="Password", private=True, required=True),
    ]
    REGISTRATION_TYPE = RegistrationType.TWO_FACTOR_CODE

    ROSTER_GROUP = "Steam"

    SEARCH_FIELDS = [
        FormField(
            var="user_name",
            label="The name of the user after https://steamcommunity.com/id",
            required=True,
        ),
    ]

    COMPONENT_NAME = "Steam (slidge)"
    COMPONENT_TYPE = "steam"

    COMPONENT_AVATAR = "https://logos-download.com/wp-content/uploads/2016/05/Steam_icon_logo_logotype.png"

    GROUPS = True

    LEGACY_MSG_ID_TYPE = int
    LEGACY_CONTACT_ID_TYPE = int
    LEGACY_ROOM_ID_TYPE = ChannelId.from_str

    def __init__(self):
        super().__init__()
        self.__pending = dict[JID, tuple[asyncio.Task, CredentialsValidation]]()

    async def validate(
        self, user_jid: JID, registration_form: dict[str, Optional[str]]
    ):
        username = registration_form["username"]
        password = registration_form["password"]

        assert isinstance(username, str)
        assert isinstance(password, str)

        client = CredentialsValidation()

        async def wrap():
            try:
                await client.login(username, password)
            except Exception as e:
                self.log.exception("Login failed for %s", user_jid, exc_info=e)

        task = self.xmpp.loop.create_task(wrap())
        self.__pending[JID(user_jid.bare)] = (task, client)
        return {}

    async def validate_two_factor_code(self, user: GatewayUser, code: str) -> dict:
        task, client = self.__pending.pop(user.jid)
        client.code_future.set_result(code)
        try:
            await asyncio.wait_for(asyncio.shield(client.wait_until_ready()), 5)
            if task.done() and (exc := task.exception()):
                raise XMPPError("not-authorized", f"That didn't work: {exc}")
            await asyncio.wait_for(client.wait_until_ready(), 60)
        except (asyncio.TimeoutError, asyncio.CancelledError):
            raise XMPPError("not-authorized", f"Authorization timed out")
        await client.wait_until_ready()
        token = client.refresh_token
        await client.close()
        # For unknown reason, closing and re-opening the connection right away hangs,
        # waiting is a dirty but mostly functional workaround.
        await asyncio.sleep(10)
        return {"refresh_token": token}


log = logging.getLogger(__name__)
