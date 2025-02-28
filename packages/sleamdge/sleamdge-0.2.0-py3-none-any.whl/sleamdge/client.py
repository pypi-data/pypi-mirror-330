import asyncio
import logging
from asyncio import Future, get_running_loop
from datetime import datetime
from typing import TYPE_CHECKING, Generic, Optional, TypeVar, Union

import steam
from slixmpp.exceptions import XMPPError

if TYPE_CHECKING:
    from .contact import Contact
    from .group import Participant
    from .session import Session


ClanOrGroup = Union[steam.Clan, steam.Group]
Channel = Union[steam.GroupChannel, steam.ClanChannel]


class CredentialsValidation(steam.Client):
    """
    A client for entering the OTP interactively and validating credentials
    """

    def __init__(self, **k) -> None:
        super().__init__(**k)
        self.code_future: Future[str] = get_running_loop().create_future()

    async def code(self) -> str:
        return await self.code_future


class SteamClient(steam.Client):
    """
    The main steam client of registered users
    """

    def __init__(self, session: "Session", **k) -> None:
        self.session = session
        self.__outbox = Pending[int]()
        self.__outbox_reaction = Pending[tuple[int, str, bool]]()
        super().__init__(**k)

    async def code(self) -> str:
        return await self.session.input(
            "You have been disconnected, please enter the code "
            "you received via email or steam guard"
        )

    async def get_contact_or_participant(
        self, message: steam.Message
    ) -> Optional[Union["Contact", "Participant"]]:
        if isinstance(message, steam.UserMessage):
            return await self.session.contacts.by_steam_user(
                message.channel.participant
            )
        elif isinstance(message, (steam.GroupMessage, steam.ClanMessage)):
            muc = await self.session.bookmarks.by_steam_channel(message.channel)
            return await muc.get_participant_by_legacy_id(message.author.id)
        return None

    async def on_typing(self, user: steam.User, when: datetime):
        if user == self.user:
            return
        c = await self.session.contacts.by_steam_user(user)
        c.composing()

    async def on_message(self, message: steam.Message) -> None:
        if self.__outbox.set_if_pending(message.id):
            return

        c = await self.get_contact_or_participant(message)
        if c is None:
            return

        c.send_text(
            message.clean_content, message.id, carbon=message.author == self.user
        )

    async def on_reaction_add(self, reaction: steam.MessageReaction) -> None:
        if not reaction.emoticon:
            return
        if self.__outbox_reaction.set_if_pending(
            (reaction.message.id, reaction.emoticon.name, True)
        ):
            return
        await self.update_reactions(reaction)

    async def on_reaction_remove(self, reaction: steam.MessageReaction) -> None:
        if not reaction.emoticon:
            return
        if self.__outbox_reaction.set_if_pending(
            (reaction.message.id, reaction.emoticon.name, False)
        ):
            return

        await self.update_reactions(reaction)

    async def on_clan_update(self, before: steam.Clan, after: steam.Clan, /) -> None:
        await self.on_group_or_clan_update(before, after)

    async def on_clan_join(self, clan: steam.Clan, /) -> None:
        for c in clan.channels:
            await self.session.bookmarks.by_steam_channel(c)

    async def on_clan_leave(self, clan: steam.Clan, /) -> None:
        # TODO:
        pass

    async def on_group_update(self, before: steam.Group, after: steam.Group, /) -> None:
        await self.on_group_or_clan_update(before, after)

    async def on_group_or_clan_update(
        self, before: ClanOrGroup, after: ClanOrGroup, /
    ) -> None:
        channels_before = set[Channel](before.channels)
        channels_after = set[Channel](after.channels)

        for channel in channels_after - channels_before:
            muc = await self.session.bookmarks.by_steam_channel(channel)
            if isinstance(after, steam.Group):
                await muc.add_to_bookmarks()
        for channel in channels_before - channels_after:
            muc = await self.session.bookmarks.by_steam_channel(channel)
            muc.get_system_participant().send_text(
                "This channel has been destroyed but this is not yet implemented in slidge…"
            )

        existing_mucs = [
            await self.session.bookmarks.by_steam_channel(c) for c in channels_before
        ]

        for muc in existing_mucs:
            await muc.update_info()

    async def on_group_join(self, group: steam.Group, /) -> None:
        for c in group.channels:
            muc = await self.session.bookmarks.by_steam_channel(c)
            await muc.add_to_bookmarks()

    async def on_group_leave(self, group: steam.Group, /) -> None:
        # TODO:
        pass

    async def update_reactions(self, reaction: steam.MessageReaction) -> None:
        message = reaction.message
        if not reaction.emoticon:
            return
        c = await self.get_contact_or_participant(message)
        if c is None:
            return

        self.session.log.debug("Reaction: %s", reaction)
        await c.update_reaction(reaction)

    async def on_user_update(self, before: steam.User, after: steam.User) -> None:
        if after.id == self.user.id:
            return
        c = await self.session.contacts.by_steam_user(after)
        await c.update_info(after)

    async def add_emoticon(self, msg: steam.Message, emoticon: steam.Emoticon) -> None:
        e = self.__outbox_reaction.place((msg.id, emoticon.name, True))
        await msg.add_emoticon(emoticon)
        await e.wait()

    async def remove_emoticon(
        self, msg: steam.Message, emoticon: steam.Emoticon
    ) -> None:
        e = self.__outbox_reaction.place((msg.id, emoticon.name, False))
        await msg.remove_emoticon(emoticon)
        await e.wait()

    async def send(
        self,
        recipient: Union[steam.User, steam.GroupChannel, steam.ClanChannel],
        text: str,
    ) -> int:
        message = await recipient.send(text)
        if message is None:
            raise XMPPError("internal-server-error", "No message ID")
        e = self.__outbox.place(message.id)
        await e.wait()
        return message.id

    async def fetch_user_named(self, name: str):
        id64 = await steam.utils.id64_from_url(
            f"https://steamcommunity.com/id/{name}", self.session.http
        )
        return await self._state.fetch_user(id64) if id64 is not None else None


T = TypeVar("T")


class Pending(Generic[T]):
    """
    Helper for the fact that everything we send is echoed, and we mostly
    want to ignore echoes/
    """

    def __init__(self) -> None:
        self.__data = dict[T, asyncio.Event]()

    def place(self, key: T) -> asyncio.Event:
        e = self.__data[key] = asyncio.Event()
        return e

    def set_if_pending(self, key: T) -> bool:
        e = self.__data.pop(key, None)
        if e is None:
            return False
        e.set()
        return True


log = logging.getLogger(__name__)
