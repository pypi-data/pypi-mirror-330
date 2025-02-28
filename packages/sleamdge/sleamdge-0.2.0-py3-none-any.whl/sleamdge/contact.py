from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator, Optional

import steam
from slidge import LegacyContact, LegacyRoster
from slixmpp.exceptions import XMPPError
from steam.types.id import ID32

from .util import EMOJIS_SET, emojize

if TYPE_CHECKING:
    from .session import Session


class Roster(LegacyRoster[ID32, "Contact"]):
    session: "Session"

    async def by_steam_user(self, user: steam.User) -> Contact:
        return await self.by_legacy_id(user.id)

    async def jid_username_to_legacy_id(self, local: str) -> ID32:
        try:
            local_int = int(local)
        except ValueError:
            raise XMPPError("bad-request", f"This is not a valid integer: {local}")
        return ID32(local_int)

    async def fill(self) -> AsyncIterator["Contact"]:
        for user in await self.session.steam.user.friends():
            c = await self.by_steam_user(user)
            c.is_friend = True
            yield c


class Contact(LegacyContact[ID32]):
    MARKS = False
    CORRECTION = False
    RETRACTION = False

    session: "Session"

    async def get_steam_channel(self) -> steam.User:
        u = self.session.steam.get_user(self.legacy_id)
        if u is None:
            raise XMPPError("item-not-found")
        return u

    async def update_info(self, user: Optional[steam.User] = None) -> None:
        if user is None:
            user = await self.get_steam_channel()
        self.name = user.name
        self.avatar = user.avatar.url
        await self.update_state(user)

    async def update_state(self, user: Optional[steam.User] = None) -> None:
        if user is None:
            user = await self.get_steam_channel()
        self.log.debug("Rich presence: %s", user.rich_presence)
        match user.state:
            case steam.PersonaState.Online:
                self.online()
            case steam.PersonaState.Offline:
                if user.last_seen_online:
                    # workaround for gajim not parsing last presence for "unavailable"
                    self.extended_away(last_seen=user.last_seen_online)
                else:
                    self.offline()
            case steam.PersonaState.Busy:
                self.busy(last_seen=user.last_seen_online)
            case steam.PersonaState.Away:
                self.away(last_seen=user.last_seen_online)
            case steam.PersonaState.Snooze:
                self.extended_away(last_seen=user.last_seen_online)
            case steam.PersonaState.LookingToPlay:
                self.online(status="Looking to play", last_seen=user.last_seen_online)
            case steam.PersonaState.LookingToTrade:
                self.online(status="Looking to trade", last_seen=user.last_seen_online)

    async def available_emojis(self, legacy_msg_id=None) -> set[str]:
        return EMOJIS_SET

    async def update_reaction(self, reaction: steam.MessageReaction) -> None:
        user = self.session.steam.user
        carbon = reaction.user == user
        self.log.debug("Reaction: carbon: %s - %s - %s", user, reaction.user, carbon)
        message = await self.fetch_message(reaction.message.id)

        reactions = list[str]()
        for r in message.reactions:
            if emoticon := r.emoticon:
                emoji = emojize(emoticon)
                self.log.debug("UPDATING R: %s %s %s", emoji, r.user, user)
                if r.user == user and carbon:
                    reactions.append(emoji)
                elif r.user != user and not carbon:
                    reactions.append(emoji)
        self.log.debug("UPDATING RS: %s %s %s", message.id, reactions, carbon)
        self.react(message.id, reactions, carbon=carbon)

    async def fetch_message(self, legacy_msg_id: int) -> steam.UserMessage:
        msg = await (await self.get_steam_channel()).fetch_message(legacy_msg_id)
        if msg is None:
            raise XMPPError(
                "item-not-found", f"Could not find the legacy message {legacy_msg_id}"
            )
        if not isinstance(msg, steam.UserMessage):
            raise XMPPError(
                "internal-server-error", f"This is not a 1:1 message: '{type(msg)}'"
            )
        return msg
