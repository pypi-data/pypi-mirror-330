import asyncio
import html
import json
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Optional

from mattermost_api_reference_client.models import (
    Status,
    UpdateUserCustomStatusJsonBody,
    User,
)
from mattermost_api_reference_client.types import Unset
from slidge import LegacyContact, LegacyRoster

from .events import StatusType
from .util import UserMixin, emojize_single

if TYPE_CHECKING:
    from .session import Session


async def noop():
    pass


class Contact(UserMixin, LegacyContact[str]):
    session: "Session"
    STATUS_FETCH_MINIMUM_INTERVAL = timedelta(seconds=10)
    STATUS_API_FETCH_MINIMUM_INTERVAL = timedelta(seconds=60)

    MARKS = False
    REPLIES = False

    def __init__(
        self,
        session: "Session",
        legacy_id: str,
        jid_username: str,
        user: Optional[User] = None,
    ):
        super().__init__(session, legacy_id, jid_username)

        # the concept of status in mattermost is quite complex
        # - the status is the <presence show= and needs to be fetched manually
        # - "custom status" which is the <presence><status>
        # - they don't arrive together, so we need to cache them
        self._status: StatusType = "online"
        self._last_seen: Optional[datetime] = None
        self._custom_status: Optional[str] = None

        self._last_status_fetch: Optional[datetime] = None
        self._last_api_status_fetch: Optional[datetime] = None
        self.mm = self.session.mm_client
        self.mm_user = user

    def serialize_extra_attributes(self) -> Optional[dict]:
        return {
            "last_seen": dt_to_iso_or_none(self._last_seen),
            "custom_status": self._custom_status,
            "last_status_fetch": dt_to_iso_or_none(self._last_status_fetch),
            "last_api_status_fetch": dt_to_iso_or_none(self._last_api_status_fetch),
        }

    def deserialize_extra_attributes(self, data: dict) -> None:
        self._custom_status = data.get("custom_status")
        self._last_seen = str_or_none_to_dt(data.get("last_seen"))
        self._last_status_fetch = str_or_none_to_dt(data.get("last_status_fetch"))
        self._last_api_status_fetch = str_or_none_to_dt(
            data.get("last_api_status_fetch")
        )

    async def on_friend_request(self, text=""):
        # Everybody is a 'friend' on mattermost, but to avoid cluttering
        # the roster, we only add users with whom the user has a direct
        # channel.
        # But if the user decide to add manually a contact, we set the
        # is_friend flag so the user gets updates for presence, avatar, nick…
        self.is_friend = True

    def update_websocket_status(self, status: StatusType):
        # Via the websocket we only get online, away, etc.
        self._last_status_fetch = datetime.now()
        self._status = status
        self._update_presence()

    def update_custom_status(self, c: Optional[UpdateUserCustomStatusJsonBody] = None):
        # Custom status are part of the User model, returned by
        # get_user or as part of the UserUpdate event, and also
        # part of the status returned by
        self.log.debug("Update custom status: %s", c)
        if not c:
            self._custom_status = None
            self.session.contacts.unschedule_status_expiration(self.legacy_id)
            self._update_presence()
            if not self._updating_info:
                self.xmpp.store.contacts.update(self)
            return

        if c.emoji:
            e = emojize_single(c.emoji)
            parts = [e, c.text]
        else:
            parts = [html.unescape(c.text)]
        self._custom_status = " ".join(parts)

        if expire_str := c.expires_at:
            try:
                expires_in = (
                    datetime.fromisoformat(expire_str) - datetime.now(UTC)
                ).seconds
            except ValueError:
                self.log.warning("Could not convert %s to a datetime", expire_str)
            else:
                self.session.contacts.schedule_status_expiration(
                    self.legacy_id, expires_in
                )
        if not self._updating_info:
            self.xmpp.store.contacts.update(self)
        self._update_presence()

    async def fetch_status(self):
        # The "API call" (=http get request) contains more information, such as
        # last_seen (but not "custom status"), but we shouldn't poll for it too often.
        if not await self.fetch_api_status():
            # if we polled to recently via GET, let's just make a WS fetch for "online",
            # "away" or "dnd".
            await self.fetch_ws_status()

    async def fetch_ws_status(self) -> bool:
        # In previous versions, I suspected this killed the websocket, but this was
        # possibly a wrong lead. Disable me if we run into trouble!
        if self._last_status_fetch:
            now = datetime.now()
            delay = now - self._last_status_fetch
            if delay < self.STATUS_FETCH_MINIMUM_INTERVAL:
                self.log.debug("Not fetching status: %s", delay)
                return False
        mm_id = await self.mm_id()
        status = await self.session.ws.get_statuses_by_ids([mm_id])
        self.update_websocket_status(status[mm_id])
        return True

    async def fetch_api_status(self) -> bool:
        if self._last_api_status_fetch:
            now = datetime.now()
            delay = now - self._last_api_status_fetch
            if delay < self.STATUS_API_FETCH_MINIMUM_INTERVAL:
                self.log.debug("Not fetching api status: %s", delay)
                return False
        mm_id = await self.mm_id()
        status = await self.mm.get_user_status(mm_id)
        if status:
            self.update_api_status(status)
        return status is not None

    async def _reset_custom_status(self, sleep: float):
        self.log.debug("Clearing custom status in %s", sleep)
        await asyncio.sleep(sleep)
        self.log.debug("Clearing custom status")
        self.update_custom_status(None)

    def update_api_status(self, status: Status):
        # if we fetch via the HTTP API get_user_status, we get a status object,
        # with the last seen info
        self.log.debug("Updating status from HTTP call: %s", status)
        self._status = status.status  # type:ignore
        self._last_api_status_fetch = datetime.now()
        self._last_seen = (
            datetime.fromtimestamp(status.last_activity_at / 1000)
            if status.last_activity_at
            else None
        )
        self._update_presence()

    def _update_presence(self):
        status = self._status
        text = self._custom_status
        if self._status != "online":
            last_seen = self._last_seen
        else:
            last_seen = None
        self.log.debug("Updating presence: %s %s %s", status, text, last_seen)
        if status == "online":
            self.online(text, last_seen=last_seen)
        elif status == "offline":
            # We use extended away instead of offline because gajim does not parse
            # status and last_seen for 'offline' presences.
            # https://dev.gajim.org/gajim/gajim/-/issues/11514
            self.extended_away(text, last_seen=last_seen)
        elif status == "away":
            self.away(text, last_seen=last_seen)
        elif status == "dnd":
            self.busy(text, last_seen=last_seen)
        else:
            self.session.log.warning("Unknown status for '%s':", status)

    async def direct_channel_id(self):
        return await self.mm.get_direct_channel_id(await self.mm_id())

    async def mm_id(self):
        return await self.mm.get_user_id_by_username(self.legacy_id)

    async def update_info(self, user: Optional[User] = None):
        if user is None:
            if self.mm_user is not None:
                self.log.debug("No need to fetch!")
                user = self.mm_user
            else:
                user = await self.mm.get_user(await self.mm_id())

        full_name = " ".join(
            filter(None, [user.first_name, user.last_name])  # type:ignore
        ).strip()

        self.name = user.nickname or full_name

        self.set_vcard(
            full_name=full_name,
            given=user.first_name,  # type:ignore
            surname=user.last_name,  # type:ignore
            email=user.email,  # type:ignore
        )

        last_update = user.last_picture_update
        uid = f"{user.id}-{'Unset' if isinstance(last_update, Unset) else last_update}"
        if self.avatar != uid:
            self.log.debug("We need to download avatar: %s vs %s", self.avatar, uid)
            await self.set_avatar(await self.mm.get_profile_image(user.id), uid)
        else:
            self.log.debug("Cached avatar is OK")

        props = user.props
        if not props:
            return

        custom_dict = props.additional_properties.get("customStatus")

        if custom_dict:
            custom_status = UpdateUserCustomStatusJsonBody.from_dict(
                json.loads(custom_dict)
            )
        else:
            custom_status = None

        self.update_custom_status(custom_status)


class Roster(LegacyRoster[str, Contact]):
    session: "Session"

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        # keys = contact legacy IDs
        self.__status_expiration_tasks = dict[str, asyncio.Task]()

    @property
    def mm(self):
        return self.session.mm_client

    def schedule_status_expiration(self, legacy_id: str, sleep: float):
        self.unschedule_status_expiration(legacy_id)
        self.__status_expiration_tasks[legacy_id] = self.session.create_task(
            self.__expire_status(legacy_id, sleep)
        )

    def unschedule_status_expiration(self, legacy_id: str):
        existing = self.__status_expiration_tasks.pop(legacy_id, None)
        if existing is not None:
            existing.cancel()

    async def __expire_status(self, legacy_id: str, sleep: float):
        self.log.debug("Clearing custom status of %s in %s", legacy_id, sleep)
        await asyncio.sleep(sleep)
        self.log.debug("Clearing custom status of %s", legacy_id)
        contact = await self.by_legacy_id(legacy_id)
        contact.update_custom_status(None)

    async def by_jid(self, jid):
        c: Contact = await super().by_jid(jid)
        if c.is_friend:
            await c.fetch_status()
        return c

    async def by_legacy_id(
        self, legacy_id: str, user: Optional[User] = None, *a, **kw
    ) -> Contact:
        c: Contact = await super().by_legacy_id(legacy_id, user)
        if c.is_friend:
            await c.fetch_status()
        return c

    async def by_mm_user_id(self, user_id: str, user: Optional[User] = None) -> Contact:
        if user:
            assert user.username
            username = user.username
        else:
            username = await self.mm.get_username_by_user_id(user_id)
        return await self.by_legacy_id(username, user)

    async def by_direct_channel_id(self, channel_id: str) -> Optional[Contact]:
        username = await self.mm.get_other_username_from_direct_channel_id(channel_id)
        if not username:
            return None
        return await self.by_legacy_id(username)

    async def fill(self):
        mm = self.mm
        user_ids = await mm.get_contacts()
        if not user_ids:
            return
        users = {
            user.username: user for user in await self.mm.get_users_by_ids(user_ids)
        }
        self.log.debug("Fetched %s users at once", len(users))

        for username, user in users.items():
            contact = await self.by_legacy_id(username, user)
            contact.is_friend = True
            yield contact

    async def known_user_ids(self, only_friends=False, including_me=True):
        me = await self.mm.mm_id
        known_contacts = self.session.contacts.known_contacts(
            only_friends=only_friends
        ).items()
        r = [await c.mm_id() for _jid, c in known_contacts if await c.mm_id() != me]
        if including_me:
            r.append(me)
        return r


def dt_to_iso_or_none(dt: datetime | None):
    if dt is None:
        return None
    return dt.isoformat()


def str_or_none_to_dt(string: str | None):
    if string is None:
        return None
    return datetime.fromisoformat(string)
