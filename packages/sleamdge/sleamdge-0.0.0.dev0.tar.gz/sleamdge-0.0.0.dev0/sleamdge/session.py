import asyncio
import tempfile
from io import BytesIO
from typing import Optional, Union

import steam
from PIL import Image
from slidge import BaseSession, FormField, SearchResult, global_config
from slixmpp.exceptions import XMPPError

from .client import SteamClient
from .contact import Contact, Roster
from .group import MUC, Bookmarks
from .util import demojize, emojize

Recipient = Union[Contact, MUC]


class Session(BaseSession[int, Recipient]):
    contacts: Roster
    bookmarks: Bookmarks

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.steam = SteamClient(self)
        self.login_task: Optional[asyncio.Task] = None
        self.emoticons = dict[str, steam.Emoticon]()

    @staticmethod
    def xmpp_to_legacy_msg_id(i: str) -> int:
        return int(i)

    async def __login_task(self):
        refresh_token = self.user.legacy_module_data.get("refresh_token")
        if refresh_token is None:
            refresh_token = (
                global_config.HOME_DIR / str(self.user_jid.bare)
            ).read_text()
            self.legacy_module_data_set({"refresh_token": refresh_token})
        assert isinstance(refresh_token, str)

        try:
            async with self.steam:
                await self.steam.login(refresh_token=refresh_token)
        except Exception as e:
            self.log.debug("logged out", exc_info=e)
            self.send_gateway_status("Logged out", show="dnd")
            self.send_gateway_message(
                f"You have been logged out ('{e}').\n"
                f"This may be because you have logged in to steam from another client.\n"
                f"Use the 're-login' command when you want to log back in from here."
            )
            self.steam = SteamClient(self)
            self.logged = False

    async def login(self) -> None:
        self.login_task = asyncio.create_task(self.__login_task())
        await self.steam.wait_until_ready()
        self.contacts.user_legacy_id = self.steam.user.id
        self.emoticons = {e.name: e for e in self.steam.emoticons}

    async def logout(self) -> None:
        await self.steam.close()

    async def on_composing(self, c: Recipient, thread=None) -> None:
        if c.is_group:
            return
        assert isinstance(c, Contact)
        user = await c.get_steam_channel()
        await user.trigger_typing()

    async def on_text(self, chat: Recipient, text: str, **_kwargs) -> int:
        recipient = await chat.get_steam_channel()
        mid = await self.steam.send(recipient, text)
        return mid

    async def on_file(self, chat: Recipient, url: str, **_kwargs) -> int:
        recipient = await chat.get_steam_channel()
        mid = await self.steam.send(recipient, url)
        return mid

    async def on_react(
        self, chat: Recipient, legacy_msg_id: int, emojis: list[str], thread=None
    ) -> None:
        msg = await chat.fetch_message(legacy_msg_id)

        reactions_xmpp = set(emojis)
        reactions_steam = set()
        for r in msg.reactions:
            if emoticon := r.emoticon:
                if r.user == self.steam.user:
                    reactions_steam.add(emojize(emoticon))

        to_remove = reactions_steam - reactions_xmpp
        to_add = reactions_xmpp - reactions_steam

        self.log.debug("msg: %s", msg)

        for emoji in to_add:
            emoticon_name = demojize(emoji)
            if emoticon_name is None:
                raise XMPPError("bad-request", f"Forbidden emoji: {emoji}")
            emoticon = self.emoticons[emoticon_name]
            self.log.debug("add emoticon: %r", emoticon)
            await self.steam.add_emoticon(msg, emoticon)

        for emoji in to_remove:
            emoticon_name = demojize(emoji)
            emoticon = self.emoticons[emoticon_name]
            self.log.debug("rm emoticon: %r", emoticon)
            await self.steam.remove_emoticon(msg, emoticon)

    async def on_correct(self, *args, **kwargs) -> None:
        raise XMPPError("feature-not-implemented", "No correction in steam")

    async def on_retract(
        self, chat: Recipient, legacy_msg_id: int, thread=None
    ) -> None:
        raise XMPPError("feature-not-implemented", "No retraction in steam")

    async def on_displayed(self, c: Recipient, legacy_msg_id: int, thread=None) -> None:
        msg = await c.fetch_message(legacy_msg_id)
        await msg.ack()

    async def on_search(self, form_values: dict[str, str]):
        user = await self.steam.fetch_user_named(form_values["user_name"])
        if not user:
            raise XMPPError("item-not-found")
        return SearchResult(
            fields=[FormField("username"), FormField("jid", type="jid-single")],
            items=[
                {
                    "username": form_values["user_name"],
                    "jid": (await self.contacts.by_steam_user(user)).jid.bare,
                }
            ],
        )

    async def on_avatar(
        self, bytes_: Optional[bytes], hash_, type_, width, height
    ) -> None:
        if bytes_ is None:
            # Steam forces you to have an avatar, so we cannot remove it AFAIK
            return
        if len(bytes_) > 10e6:
            # steam does not want avatars larger than 1024 KB
            bytes_ = await self.xmpp.loop.run_in_executor(None, resize_image, bytes_)
        # workaround for bug in steam.py preventing use of BytesIO
        # https://github.com/Gobot1234/steam.py/issues/566
        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.write(bytes_)
            await self.steam.user.edit(avatar=steam.Media(tmp_file.name))


def resize_image(bytes_: bytes) -> bytes:
    with BytesIO() as f:
        img = Image.open(BytesIO(bytes_))
        img.thumbnail((500, 500))  # should be < 1024 KB hopefully
        img.save(f, format="JPEG")
        f.flush()
        f.seek(0)
        return f.read()
