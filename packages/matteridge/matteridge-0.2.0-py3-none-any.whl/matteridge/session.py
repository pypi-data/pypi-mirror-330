import asyncio
import re
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Concatenate,
    Optional,
    ParamSpec,
    TypeVar,
    Union,
)

from slidge import BaseSession
from slidge.util.types import PseudoPresenceShow, ResourceDict
from slixmpp.exceptions import XMPPError

from . import events
from .api import MattermostException, get_client_from_registration_form
from .util import emojize_single
from .websocket import Websocket

if TYPE_CHECKING:
    from .contact import Contact, Roster
    from .gateway import Gateway
    from .group import MUC, Bookmarks


Recipient = Union["Contact", "MUC"]
P = ParamSpec("P")
T = TypeVar("T", bound=Awaitable)


def lock(
    meth: Callable[Concatenate["Session", P], T],
) -> Callable[Concatenate["Session", P], T]:
    async def wrapped(self, *a, **k):
        async with self.send_lock:
            return await meth(self, *a, **k)

    return wrapped


def catch_expired_session(
    meth: Callable[Concatenate["Session", P], T],
) -> Callable[Concatenate["Session", P], T]:
    async def wrapped(self, *a, **k):
        try:
            return await meth(self, *a, **k)
        except MattermostException as e:
            if e.is_expired_session:
                await self.logout()
                await self.renew_token()
                await self.login()
                return await meth(self, *a, **k)
            else:
                raise

    return wrapped


class Session(BaseSession[str, Recipient]):
    contacts: "Roster"
    bookmarks: "Bookmarks"
    MESSAGE_IDS_ARE_THREAD_IDS = True
    xmpp: "Gateway"

    def __init__(self, user):
        super().__init__(user)
        self.messages_waiting_for_echo = set[str]()
        self.reactions_waiting_for_echo = set[tuple[str, str, bool]]()
        self.send_lock = asyncio.Lock()
        f = self.user.legacy_module_data
        self.mm_client = get_client_from_registration_form(f, self.xmpp.cache)  # type:ignore
        self.view_events = dict[str, asyncio.Event]()
        self._ws_task: Optional[asyncio.Task] = None

    def __init_ws(self):
        f = self.user.legacy_module_data
        self.ws = Websocket(
            re.sub("^http", "ws", f["url"].rstrip("/") or "")  # type:ignore
            + (f["basepath"] or "")
            + (f["basepath_ws"] or ""),
            f["token"],
            self.xmpp.http,
        )

    @lock
    async def is_waiting_for_echo(self, post_id: str):
        try:
            self.messages_waiting_for_echo.remove(post_id)
        except KeyError:
            return False
        else:
            return True

    @lock
    async def is_reaction_waiting_for_echo(self, post_id: str, emoji: str, add: bool):
        try:
            self.reactions_waiting_for_echo.remove((post_id, emoji, add))
        except KeyError:
            return False
        else:
            return True

    async def renew_token(self) -> bool:
        await self.logout()
        try:
            token = await self.input(
                "Your mattermost token has expired, please provide a new one."
            )
            self.logged = False
            self.send_gateway_status("Disconnected: expired token.", show="dnd")
        except XMPPError:
            self.send_gateway_message(
                "You took too much time to reply. "
                "Use the re-login command when you're ready to provide a new token."
            )
            return False
        else:
            self.update_token(token)
            return True

    def update_token(self, token: str):
        self.legacy_module_data_update({"token": token})
        self.mm_client = get_client_from_registration_form(
            self.user.legacy_module_data,  # type:ignore
            self.xmpp.cache,
        )

    async def login(self):
        try:
            await self.mm_client.login()
        except MattermostException as e:
            if not e.is_expired_session:
                raise
            renewed = await self.renew_token()
            if renewed:
                await self.mm_client.login()
            else:
                raise
        self.__init_ws()
        self.contacts.user_legacy_id = (await self.mm_client.me).username
        self._ws_task = asyncio.create_task(self.ws.connect(self.on_mm_event))
        self._ws_task.add_done_callback(self._websocket_fail)
        return f"Connected as '{(await self.mm_client.me).username}'"

    def _websocket_fail(self, task: asyncio.Task):
        try:
            task.exception()
        except asyncio.CancelledError:
            # logout on purpose
            return
        self.send_gateway_message(f"Oh no! The web socket connection died: {task}")
        self.logged = False
        self.send_gateway_status(
            f"Not connected to {self.user.legacy_module_data.get('url')}.", "dnd"
        )

    async def __get_contact_or_participant(self, user_id: str, channel_id: str):
        contact = await self.contacts.by_direct_channel_id(channel_id)
        if contact is not None:
            return contact
        muc = await self.bookmarks.by_legacy_id(channel_id)
        return await muc.get_participant_by_mm_user_id(user_id)

    async def on_mm_event(self, event: events.MattermostEvent):
        self.log.debug("Event: %s", event)
        handler = getattr(self, f"on_mm_{event.type.name}", None)
        if handler:
            return await handler(event)

        self.log.debug("Ignored event: %s", event.type)

    async def on_mm_DirectAdded(self, event: events.DirectAdded):
        if (teammate_id := event.teammate_id) == await self.mm_client.mm_id:
            contact_id = event.creator_id
        else:
            contact_id = teammate_id
        contact = await self.contacts.by_mm_user_id(contact_id)
        contact.is_friend = True
        await contact.add_to_roster()

    async def on_mm_Posted(self, event: events.Posted):
        post = event.post
        self.log.debug("Post: %s", post)
        user_id = post.user_id

        self.xmpp.cache.msg_id_store(
            await self.mm_client.mm_id, post.channel_id, post.id
        )

        if await self.is_waiting_for_echo(post.id):
            return

        carbon = post.user_id == await self.mm_client.mm_id
        if event.channel_type == "D":  # Direct messages
            if carbon:
                contact = await self.contacts.by_direct_channel_id(post.channel_id)
            else:
                contact = await self.contacts.by_mm_user_id(user_id)
            if not contact:
                self.log.error("Could not contact %s", user_id)
                return
            if not carbon:
                contact.update_websocket_status("online")
            await contact.send_mm_post(post, carbon)
        else:
            muc = await self.bookmarks.by_legacy_id(post.channel_id)
            if post.type == "system_add_to_channel":
                part = muc.get_system_participant()
            else:
                part = await muc.get_participant_by_mm_user_id(post.user_id)
            if not part:
                self.log.error("Could not contact %s", user_id)
                return
            if not carbon:
                part.contact.update_websocket_status("online")
            await part.send_mm_post(post)

    async def on_mm_ChannelViewed(self, event: events.ChannelViewed):
        channel_id = event.channel_id
        f = self.view_events.pop(channel_id, None)
        if f is not None:
            f.set()
            return
        last_msg_id = await self.mm_client.get_latest_post_id_for_channel(channel_id)
        if last_msg_id is None:
            self.log.debug("ChannelViewed event for a channel with no messages")
            return
        c = await self.contacts.by_direct_channel_id(channel_id)
        if c is None:
            muc = await self.bookmarks.by_legacy_id(channel_id)
            me = await muc.get_user_participant()
            me.displayed(last_msg_id)
        else:
            c.displayed(last_msg_id, carbon=True)

    async def on_mm_StatusChange(self, event: events.StatusChange):
        user_id = event.user_id
        if user_id == await self.mm_client.mm_id:
            self.log.debug("Own status change")
        else:
            contact = await self.contacts.by_mm_user_id(user_id)
            contact.update_websocket_status(event.status)

    async def on_mm_Typing(self, event: events.Typing):
        contact_or_participant = await self.__get_contact_or_participant(
            event.user_id, event.broadcast.channel_id
        )
        contact_or_participant.composing()

    async def on_mm_PostEdited(self, event: events.PostEdited):
        post = event.post
        if await self.is_waiting_for_echo(post.id):
            return
        contact_or_participant = await self.__get_contact_or_participant(
            post.user_id, post.channel_id
        )
        contact_or_participant.correct(
            post.id, post.message, carbon=post.user_id == await self.mm_client.mm_id
        )

    async def on_mm_PostDeleted(self, event: events.PostDeleted):
        post = event.post
        contact_or_participant = await self.__get_contact_or_participant(
            post.user_id, post.channel_id
        )
        contact_or_participant.retract(
            post.id, carbon=post.user_id == await self.mm_client.mm_id
        )

    async def on_mm_ChannelCreated(self, event: events.ChannelCreated):
        await self.bookmarks.by_legacy_id(event.channel_id)

    async def on_mm_ReactionAdded(self, event: events.ReactionAdded):
        await self.on_mm_reaction(event)

    async def on_mm_ReactionRemoved(self, event: events.ReactionRemoved):
        await self.on_mm_reaction(event)

    async def on_mm_reaction(
        self, event: Union[events.ReactionAdded, events.ReactionRemoved]
    ):
        if (
            event.reaction.user_id == await self.mm_client.mm_id
            and await self.is_reaction_waiting_for_echo(
                event.reaction.post_id,
                emojize_single(event.reaction.emoji_name or ""),
                isinstance(event, events.ReactionAdded),
            )
        ):
            return
        reaction = event.reaction
        legacy_msg_id = reaction.post_id
        contact_or_participant = await self.__get_contact_or_participant(
            reaction.user_id, event.broadcast.channel_id
        )
        await contact_or_participant.update_reactions(
            legacy_msg_id, carbon=reaction.user_id == await self.mm_client.mm_id
        )

    async def on_mm_UserUpdated(self, event: events.UserUpdated):
        user = event.user
        if user.id == await self.mm_client.mm_id:
            return
        c = await self.contacts.by_legacy_id(user.username, user)
        await c.update_info(user)

    async def on_mm_UserAdded(self, event: events.UserAdded):
        muc = await self.bookmarks.by_legacy_id(event.broadcast.channel_id)
        await muc.get_participant_by_mm_user_id(event.user_id)

    async def logout(self):
        if self._ws_task is not None and not self._ws_task.done():
            self._ws_task.cancel()

    @staticmethod
    async def __get_channel_id(chat: Recipient):
        if chat.is_group:
            return chat.legacy_id
        else:
            return await chat.direct_channel_id()  # type:ignore

    @catch_expired_session
    @lock
    async def on_text(self, chat: Recipient, text: str, thread=None, **k):
        channel_id = await self.__get_channel_id(chat)
        msg_id = await self.mm_client.send_message_to_channel(channel_id, text, thread)
        self.messages_waiting_for_echo.add(msg_id)
        return msg_id

    @catch_expired_session
    @lock
    async def on_file(self, chat: Recipient, url: str, http_response, thread=None, **k):
        channel_id = await self.__get_channel_id(chat)
        file_id = await self.mm_client.upload_file(channel_id, url, http_response)
        msg_id = await self.mm_client.send_message_with_file(
            channel_id, file_id, thread
        )
        self.messages_waiting_for_echo.add(msg_id)
        return msg_id

    @catch_expired_session
    async def on_active(self, c: Recipient, thread=None):
        pass

    @catch_expired_session
    async def on_inactive(self, c: Recipient, thread=None):
        pass

    @catch_expired_session
    async def on_composing(self, c: Recipient, thread=None):
        channel_id = await self.__get_channel_id(c)
        await self.ws.user_typing(channel_id)  # type:ignore

    @catch_expired_session
    async def on_paused(self, c: Recipient, thread=None):
        # no equivalent in MM, seems to have an automatic timeout in clients
        pass

    @catch_expired_session
    async def on_displayed(self, c: Recipient, legacy_msg_id: Any, thread=None):
        channel_id = await self.__get_channel_id(c)
        f = self.view_events[channel_id] = asyncio.Event()
        await self.mm_client.view_channel(channel_id)
        await f.wait()

    @catch_expired_session
    @lock
    async def on_correct(
        self,
        c: Recipient,
        text: str,
        legacy_msg_id: str,
        thread=None,
        link_previews=(),
        mentions=None,
    ):
        await self.mm_client.update_post(legacy_msg_id, text)
        self.messages_waiting_for_echo.add(legacy_msg_id)

    @catch_expired_session
    async def on_search(self, form_values: dict[str, str]):
        pass

    @catch_expired_session
    async def on_retract(self, c: Recipient, legacy_msg_id: Any, thread=None):
        await self.mm_client.delete_post(legacy_msg_id)

    @catch_expired_session
    async def on_react(
        self, c: Recipient, legacy_msg_id: Any, emojis: list[str], thread=None
    ):
        mm_reactions = await self.get_mm_reactions(
            legacy_msg_id, await self.mm_client.mm_id
        )
        xmpp_reactions = {x for x in emojis}
        self.log.debug("%s vs %s", mm_reactions, xmpp_reactions)
        for e in xmpp_reactions - mm_reactions:
            async with self.send_lock:
                await self.mm_client.react(legacy_msg_id, e)
                self.reactions_waiting_for_echo.add((legacy_msg_id, e, True))
        for e in mm_reactions - xmpp_reactions:
            async with self.send_lock:
                await self.mm_client.delete_reaction(legacy_msg_id, e)
                self.reactions_waiting_for_echo.add((legacy_msg_id, e, False))

    async def get_mm_reactions(self, legacy_msg_id: str, user_id: Optional[str]):
        return {
            x
            for i, x in await self.mm_client.get_reactions(legacy_msg_id)
            if i == user_id
        }

    @catch_expired_session
    async def on_presence(
        self,
        resource: str,
        show: PseudoPresenceShow,
        status: str,
        resources: dict[str, ResourceDict],
        merged_resource: Optional[ResourceDict],
    ):
        if not merged_resource:
            await self.mm_client.set_user_status("offline", None)
            return

        status = merged_resource["status"]

        if merged_resource["show"] in ("away", "xa"):
            await self.mm_client.set_user_status("away", status)
        elif merged_resource["show"] == "dnd":
            await self.mm_client.set_user_status("dnd", status)
        else:
            await self.mm_client.set_user_status("online", status)
