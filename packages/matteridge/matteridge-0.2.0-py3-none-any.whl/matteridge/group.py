from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional

from mattermost_api_reference_client.models import Channel, ChannelMember, Team
from slidge import LegacyBookmarks, LegacyMUC, LegacyParticipant, MucType, global_config
from slidge.util.types import HoleBound
from slixmpp.exceptions import XMPPError

from . import config
from .util import UserMixin

if TYPE_CHECKING:
    from .contact import Contact
    from .gateway import Gateway
    from .session import Session


class Bookmarks(LegacyBookmarks[str, "MUC"]):
    session: "Session"

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.channels = dict[str, Channel]()

    async def fill(self):
        channels = await self.session.mm_client.get_channels()
        for c in channels:
            if c.type == "D":
                continue
            await self.by_legacy_id(c.id)


class Participant(UserMixin, LegacyParticipant):
    contact: "Contact"

    def mm_id(self):
        if self.is_user:
            return self.session.mm_client.mm_id
        return self.contact.mm_id()


class MUC(LegacyMUC[str, str, Participant, str]):
    session: "Session"
    xmpp: "Gateway"

    async def update_info(self, channel: Optional[Channel] = None):
        if channel is None:
            channel = self.session.bookmarks.channels.pop(self.legacy_id, None)
            if not channel:
                channel = await self.fetch_channel()

        if channel.team_id:
            team: Team = await self.session.mm_client.get_team(channel.team_id)
            team_prefix = (team.display_name or "unnamed-team") + " / "
            await self.__set_team_icon(team)
        else:
            team_prefix = ""

        self.name = team_prefix + (channel.display_name or channel.name or "")
        self.description = channel.purpose or ""
        self.subject = channel.header or ""

        self.log.debug("Channel type: %s", channel.type)
        if channel.type == "P":
            self.type = MucType.GROUP
            await self.add_to_bookmarks(auto_join=True)
        elif channel.type == "G":
            self.type = MucType.CHANNEL_NON_ANONYMOUS
            await self.add_to_bookmarks(auto_join=True)
        elif channel.type == "O":
            self.type = MucType.CHANNEL_NON_ANONYMOUS
        else:
            self.log.warning("Unknown channel type: %s", channel.type)

        stats = await self.session.mm_client.get_channel_stats(self.legacy_id)
        self.n_participants = stats.member_count or None

    async def __set_team_icon(self, team: Team):
        uid = f"{team.id}-{team.update_at}"
        if self.avatar != uid:
            icon_bytes = await self.session.mm_client.get_team_icon(team.id)
            if icon_bytes:
                await self.set_avatar(icon_bytes, uid)
            else:
                self.avatar = None

    async def fetch_channel(self) -> Channel:
        c = await self.session.mm_client.get_channel(self.legacy_id)
        if c is None:
            raise XMPPError("item-not-found")
        return c

    async def fill_participants(self):
        users_ids = set()
        async for member in self.session.mm_client.get_channel_members(self.legacy_id):
            member: ChannelMember  # type:ignore
            users_ids.add(member.user_id)

        known = set(await self.session.contacts.known_user_ids())
        self.log.debug("Known %s", known)
        missing = users_ids - known
        if missing:
            users = {
                u.id: u
                for u in await self.session.mm_client.get_users_by_ids(list(missing))
            }
            self.log.debug("Fetched %s users at once", len(users))
        else:
            users = {}
        for user_id in users_ids:
            if user_id == await self.session.mm_client.mm_id:
                continue
            contact = await self.session.contacts.by_mm_user_id(
                user_id, users.get(user_id)
            )
            yield await self.get_participant_by_contact(contact)

    async def backfill(
        self,
        after: Optional[HoleBound] = None,
        before: Optional[HoleBound] = None,
    ):
        if not config.BACKFILL_POSTS:
            return
        now = datetime.now()
        i = 0
        self.log.info("Backfill request between %s and %s", before, after)
        before_id = None if before is None else before.id
        after_id = None if after is None else after.id
        async for post in self.session.mm_client.get_posts_for_channel(
            self.legacy_id, before=before_id
        ):
            if post.id == after_id:
                break

            if i == 0 and not self.xmpp.cache.msg_id_get(
                await self.session.mm_client.mm_id, self.legacy_id
            ):
                self.xmpp.cache.msg_id_store(
                    await self.session.mm_client.mm_id, self.legacy_id, post.id
                )
            if now - datetime.fromtimestamp(post.create_at / 1000) > timedelta(
                days=global_config.MAM_MAX_DAYS
            ):
                break
            part = await self.get_participant_by_mm_user_id(post.user_id)
            await part.send_mm_post(post, archive_only=True)
            i += 1
            if i == config.BACKFILL_POSTS:
                break

    async def get_participant_by_mm_user_id(self, user_id: str) -> "Participant":
        return await self.get_participant_by_legacy_id(
            await self.session.mm_client.get_username_by_user_id(user_id)
        )
