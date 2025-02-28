from typing import TYPE_CHECKING, AsyncIterator, Optional, Union

from slidge import LegacyBookmarks, LegacyMUC, LegacyParticipant, MucType
from slidge.util.types import HoleBound
from slixmpp.exceptions import XMPPError
from steam import (
    Clan,
    ClanChannel,
    ClanMessage,
    Group,
    GroupChannel,
    GroupMessage,
    MessageReaction,
)

from .contact import Contact
from .types import ChannelId, Parent, ParentType
from .util import EMOJIS_SET, emojize

if TYPE_CHECKING:
    from .session import Session


class Bookmarks(LegacyBookmarks[ChannelId, "LegacyMUC"]):
    session: "Session"

    async def by_steam_channel(self, channel: Union[GroupChannel, ClanChannel]):
        if channel.group:
            parent = Parent(ParentType.GROUP, channel.group.id)
        elif channel.clan:
            parent = Parent(ParentType.CLAN, channel.clan.id)
        else:
            raise XMPPError(
                "internal-server-error", "No group or clan associated to this channel"
            )
        return await self.by_legacy_id(ChannelId(parent, channel.id))

    async def legacy_id_to_jid_local_part(self, legacy_id: ChannelId) -> str:
        return str(legacy_id)

    async def jid_local_part_to_legacy_id(self, local_part: str) -> ChannelId:
        try:
            return ChannelId.from_str(local_part)
        except ValueError as e:
            raise XMPPError("bad-request", f"This is not a valid sleamdge MUC id: {e}")

    async def fill(self):
        for group in self.session.steam.groups:
            for group_channel in group.channels:
                channel_id = ChannelId(
                    Parent(ParentType.GROUP, group.id), group_channel.id
                )
                muc = await self.by_legacy_id(channel_id)
                await muc.add_to_bookmarks()
        for clan in self.session.steam.clans:
            for clan_channel in clan.channels:
                channel_id = ChannelId(
                    Parent(ParentType.CLAN, clan.id), clan_channel.id
                )
                await self.by_legacy_id(channel_id)


class Participant(LegacyParticipant):
    contact: Contact
    muc: "MUC"
    session: "Session"

    async def update_reaction(self, reaction: MessageReaction) -> None:
        message = await self.muc.fetch_message(reaction.message.id)

        reactions = list[str]()
        if emoticon := reaction.emoticon:
            reactions.append(emojize(emoticon))
        for r in message.reactions:
            self.log.debug("add reaction: %s", r)
            if emoticon := r.emoticon:
                emoji = emojize(emoticon)
                self.log.debug(
                    "add reaction: %s %s %s", emoji, r.user.id, self.contact.legacy_id
                )
                if r.user.id == self.contact.legacy_id:
                    reactions.append(emoji)
        self.log.debug("updating reactions: %s %s", message.id, reactions)
        self.react(message.id, reactions)


class MUC(LegacyMUC[ChannelId, int, Participant, int]):
    session: "Session"

    async def get_steam_channel(self) -> Union[GroupChannel, ClanChannel]:
        parent_id = self.legacy_id.parent
        parent: Optional[Union[Group, Clan]]
        if parent_id.type == ParentType.GROUP:
            parent = self.session.steam.get_group(parent_id.id)
        else:
            parent = self.session.steam.get_clan(parent_id.id)
        if not parent:
            raise XMPPError("internal-server-error", "No parent for this channel")
        channel = parent.get_channel(self.legacy_id.channel_id)
        if not channel:
            raise XMPPError(
                "item-not-found",
                f"Channel {self.legacy_id.channel_id} not found in {parent}",
            )
        return channel

    async def fetch_message(
        self, legacy_msg_id: int
    ) -> Union[GroupMessage, ClanMessage]:
        msg = await (await self.get_steam_channel()).fetch_message(legacy_msg_id)
        if msg is None:
            raise XMPPError(
                "item-not-found", f"Could not find the legacy message {legacy_msg_id}"
            )
        if not isinstance(msg, (GroupMessage, ClanMessage)):
            raise XMPPError(
                "internal-server-error", f"This is not a group message: '{type(msg)}'"
            )
        return msg

    async def update_info(self):
        channel = await self.get_steam_channel()
        self.log.debug("Channel: %s", channel)
        parent: Union[Group, Clan] = channel.group  # type:ignore
        if parent is None:
            self.name = channel.name
            self.type = MucType.GROUP
            return

        self.name = f"{parent.name}/{channel.name or 'Home'}"
        self.description = parent.tagline
        sha = parent.avatar.sha.hex()
        if self.avatar != sha:
            # TODO: use avatar.url when this is fixed upstream
            await self.set_avatar(
                f"https://avatars.akamai.steamstatic.com/{sha}_256.jpg", sha
            )
        if isinstance(parent, Clan):
            self.type = MucType.CHANNEL_NON_ANONYMOUS
        else:
            self.type = MucType.GROUP

    async def fill_participants(self) -> AsyncIterator[Participant]:
        g = (await self.get_steam_channel()).group
        if not g:
            return
        try:
            for m in await g.chunk():
                yield await self.get_participant_by_legacy_id(m.id)
        except AttributeError:
            # workaround for https://github.com/Gobot1234/steam.py/issues/565
            for m in g.members:
                yield await self.get_participant_by_legacy_id(m.id)

    async def backfill(
        self,
        after: Optional[HoleBound] = None,
        before: Optional[HoleBound] = None,
    ):
        c = await self.get_steam_channel()
        async for msg in c.history(
            before=None if before is None else before.timestamp,
            after=None if after is None else after.timestamp,
        ):
            part = await self.get_participant_by_legacy_id(msg.author.id)
            part.send_text(
                msg.clean_content,
                when=msg.created_at,
                archive_only=True,
                legacy_msg_id=msg.id,
            )

    async def available_emojis(self, legacy_msg_id=None) -> set[str]:
        return EMOJIS_SET
