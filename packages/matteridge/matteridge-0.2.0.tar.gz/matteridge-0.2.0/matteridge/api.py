import asyncio
import functools
import io
import json
import logging
from time import time
from typing import (
    AsyncIterator,
    Awaitable,
    Callable,
    Optional,
    ParamSpec,
    TypeVar,
    Union,
)

import aiohttp
import emoji
from async_lru import alru_cache
from httpx import AsyncClient
from httpx import Response as HTTPResponse
from httpx import codes as http_codes
from mattermost_api_reference_client.api.channels import (
    create_direct_channel,
    get_channel,
    get_channel_members,
    get_channel_stats,
    get_channels_for_team_for_user,
    get_channels_for_user,
    view_channel,
)
from mattermost_api_reference_client.api.files import get_file, upload_file
from mattermost_api_reference_client.api.posts import (
    create_post,
    delete_post,
    get_posts_for_channel,
    update_post,
)
from mattermost_api_reference_client.api.reactions import (
    delete_reaction,
    get_reactions,
    save_reaction,
)
from mattermost_api_reference_client.api.status import (
    get_user_status,
    get_users_statuses_by_ids,
    unset_user_custom_status,
    update_user_custom_status,
    update_user_status,
)
from mattermost_api_reference_client.api.teams import (
    get_team,
    get_team_by_name,
    get_team_icon,
    get_teams_for_user,
)
from mattermost_api_reference_client.api.users import (
    get_profile_image,
    get_user,
    get_user_by_username,
    get_users_by_ids,
    login,
)
from mattermost_api_reference_client.client import AuthenticatedClient, Client
from mattermost_api_reference_client.models import (
    Channel,
    LoginJsonBody,
    Post,
    Reaction,
    StatusOK,
    UpdateUserCustomStatusJsonBody,
    UpdateUserStatusJsonBody,
    User,
    ViewChannelJsonBody,
)
from mattermost_api_reference_client.models.create_post_json_body import (
    CreatePostJsonBody,
)
from mattermost_api_reference_client.models.update_post_json_body import (
    UpdatePostJsonBody,
)
from mattermost_api_reference_client.models.upload_file_multipart_data import (
    UploadFileMultipartData,
)
from mattermost_api_reference_client.types import UNSET, File, Response, Unset
from slixmpp.exceptions import XMPPError
from slixmpp.types import ErrorConditions

from .cache import Cache
from .events import StatusType
from .util import demojize, emojize_single


class MattermostException(XMPPError):
    ERROR_TYPES: dict[int, ErrorConditions] = {
        http_codes.BAD_REQUEST: "bad-request",
        http_codes.UNAUTHORIZED: "not-authorized",
        http_codes.FORBIDDEN: "forbidden",
        http_codes.NOT_FOUND: "item-not-found",
        http_codes.SERVICE_UNAVAILABLE: "service-unavailable",
    }

    def __init__(self, resp: Response):
        content_str = resp.content.decode()
        try:
            content_dict = json.loads(content_str)
        except json.JSONDecodeError:
            text = content_str
            self.mm_error_id = None
        else:
            text = content_dict.get("message")
            self.mm_error_id = content_dict.get("id")
        super().__init__(
            self.ERROR_TYPES.get(resp.status_code, "internal-server-error"), text
        )
        self.is_expired_session = (
            self.mm_error_id == "api.context.session_expired.app_error"
        )


class RetryHTTPClient(AsyncClient):
    DEFAULT_RETRY = 5.0

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._max_request_per_second = 10
        self._last_request = 0
        self._remaining_requests = 10

    def _update_counters(self, resp: HTTPResponse):
        limit = resp.headers.get("X-Ratelimit-Limit")
        if limit:
            self._max_request_per_second = int(limit)
        remaining = resp.headers.get("X-RateLimit-Remaining")
        if remaining:
            self._remaining_requests = int(remaining)

    async def request(self, *a, **k) -> HTTPResponse:  # type:ignore
        while True:
            if self._remaining_requests < 2:
                await asyncio.sleep(1 / self._max_request_per_second)
            resp = await super().request(*a, **k)
            self._update_counters(resp)
            if resp.status_code == http_codes.TOO_MANY_REQUESTS:
                if "X-Ratelimit-Reset" in resp.headers:
                    # MM's custom rate limit header
                    sleep = time() - int(resp.headers["X-Ratelimit-Reset"])
                elif "Retry-After" in resp.headers:
                    sleep = int(resp.headers["Retry-After"])
                else:
                    sleep = self.DEFAULT_RETRY
                await asyncio.sleep(sleep)
            else:
                return resp


class ReplyAPIClient(AuthenticatedClient):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._async_client = RetryHTTPClient(
            base_url=self._base_url,
            cookies=self._cookies,
            headers=self._headers,
            timeout=self._timeout,
            verify=self._verify_ssl,
            follow_redirects=self._follow_redirects,
            **self._httpx_args,
        )


class MattermostClient:
    # TODO: this should be autogenerated using a template in mattermost_api_reference_client

    def __init__(self, base_url: str, cache: Cache, *args, **kwargs):
        self.http = client = AuthenticatedClient(base_url, *args, **kwargs)
        self.base_url = base_url
        self._cache = cache
        cache.add_server(base_url)
        self.mm_id: asyncio.Future[str] = asyncio.get_running_loop().create_future()
        self.me: asyncio.Future[User] = asyncio.get_running_loop().create_future()

        # https://discuss.python.org/t/using-concatenate-and-paramspec-with-a-keyword-argument
        # A partial would be more elegant, but we lose type-checking of the
        # return type (type checking of the params just does not work at all)
        # mypy doesn't even properly type check things here, but pycharm seems
        # to manage to understand the type hints, some of them at least
        # auth = functools.partial(call_authenticated, client=client)
        def auth(
            func: Callable[..., Awaitable[Response[T]]],
            force_json_decode=False,
            use_json_body=False,
        ) -> Callable[..., Awaitable[T]]:
            return authenticated_call(
                func,
                client,
                force_json_decode=force_json_decode,
                use_json_body=use_json_body,
            )

        def auth_bytes(
            func: Callable[..., Awaitable[Response[T]]],
            use_json_body=False,
            return_none_when_not_found=False,
        ) -> Callable[..., Awaitable[bytes]]:
            return authenticated_call_return_content(
                func,
                client,
                use_json_body=use_json_body,
                return_none_when_not_found=return_none_when_not_found,
            )

        self._get_user = auth(get_user.asyncio_detailed)
        self.get_user_status = auth(get_user_status.asyncio_detailed)
        self._get_users_by_ids = auth(
            get_users_by_ids.asyncio_detailed, use_json_body=True
        )
        self.get_users_statuses_by_ids = auth(
            get_users_statuses_by_ids.asyncio_detailed, use_json_body=True
        )
        self._get_user_by_username = auth(
            get_user_by_username.asyncio_detailed,
        )
        self._update_user_custom_status = auth(
            update_user_custom_status.asyncio_detailed, use_json_body=True
        )
        self._update_user_status = auth(
            update_user_status.asyncio_detailed, use_json_body=True
        )

        self.get_team = auth(get_team.asyncio_detailed)
        self.get_teams_for_user = auth(get_teams_for_user.asyncio_detailed)
        self.get_team_by_name = auth(get_team_by_name.asyncio_detailed)

        self.create_direct_channel = auth(
            create_direct_channel.asyncio_detailed, use_json_body=True
        )
        self.get_channel = auth(get_channel.asyncio_detailed)
        self.get_channel_members = paginated(auth(get_channel_members.asyncio_detailed))
        self.get_channels_for_user = auth(get_channels_for_user.asyncio_detailed)
        self.get_channels_for_team_for_user = auth(
            get_channels_for_team_for_user.asyncio_detailed
        )
        self.get_channel_stats = auth(get_channel_stats.asyncio_detailed)
        self._view_channel = auth(view_channel.asyncio_detailed, use_json_body=True)

        self.create_post = auth(create_post.asyncio_detailed, use_json_body=True)
        self.delete_post = auth(delete_post.asyncio_detailed)
        self._get_posts_for_channel = auth(get_posts_for_channel.asyncio_detailed)
        self._update_post = auth(update_post.asyncio_detailed, use_json_body=True)

        self.get_profile_image = auth_bytes(get_profile_image.asyncio_detailed)
        self.get_file = auth_bytes(get_file.asyncio_detailed)
        # since we are going to fetch the team icon for each MUC (=channel),
        # let's cache it. and since it's images, let's not cache it forever
        self.get_team_icon: Callable[[str], Awaitable[Optional[bytes]]] = alru_cache(
            maxsize=100, ttl=600
        )(
            auth_bytes(  # type:ignore
                get_team_icon.asyncio_detailed,
                return_none_when_not_found=True,
            )
        )

        self._save_reaction = auth(save_reaction.asyncio_detailed, use_json_body=True)
        self._get_reactions = auth(get_reactions.asyncio_detailed)
        self._delete_reaction = auth(delete_reaction.asyncio_detailed)

    @staticmethod
    async def get_token(base_url: str, login_id: str, password: str):
        client = Client(base_url)
        resp = await login.asyncio_detailed(
            json_body=LoginJsonBody(login_id=login_id, password=password), client=client
        )
        raise_maybe(resp)
        return resp.headers["Token"]

    async def login(self):
        log.debug("Login")
        me = await self.get_user("me")
        my_id = me.id
        if not my_id:
            raise RuntimeError("Could not login")
        try:
            self.me.set_result(me)
            self.mm_id.set_result(my_id)
        except asyncio.InvalidStateError:
            # if re-login is called
            pass
        log.debug("Me: %s", me)

    async def get_user(self, user_id: str) -> User:
        user = await self._get_user(user_id)
        assert user.id
        assert user.username
        self._cache.add_user(self.base_url, user.id, user.username)
        return user

    async def get_user_by_username(self, username: str) -> User:
        user = await self._get_user_by_username(username)
        assert user.id
        assert user.username
        self._cache.add_user(self.base_url, user.id, user.username)
        return user

    async def get_users_by_ids(self, user_ids: list[str]) -> list[User]:
        users = await self._get_users_by_ids(user_ids)
        for u in users:
            assert u.id
            assert u.username
            self._cache.add_user(self.base_url, u.id, u.username)
        return users

    async def get_username_by_user_id(self, user_id: str) -> str:
        cached = self._cache.get_by_user_id(self.base_url, user_id)
        if cached and cached.username:
            return cached.username
        user = await self.get_user(user_id)
        return user.username  # type:ignore

    async def get_user_id_by_username(self, username: str) -> str:
        cached = self._cache.get_by_username(self.base_url, username)
        if cached and cached.user_id:
            return cached.user_id
        user = await self.get_user_by_username(username)
        return user.id  # type:ignore

    async def get_other_username_from_direct_channel_id(
        self, channel_id: str
    ) -> Optional[str]:
        cached = self._cache.get_user_by_direct_channel_id(
            self.base_url, await self.mm_id, channel_id
        )
        if not cached:
            return None
        if not cached.username:
            return await self.get_username_by_user_id(cached.user_id)
        return cached.username

    async def __get_other_user_id_from_direct_channel_name(self, channel: Channel):
        assert channel.name
        for user_id in channel.name.split("__"):
            if user_id != await self.mm_id:
                cached_user = self._cache.get_by_user_id(self.base_url, user_id)
                if cached_user is None:
                    username = await self.get_username_by_user_id(user_id)
                    self._cache.add_user(self.base_url, user_id, username)
                assert channel.id
                self._cache.add_direct_channel(
                    self.base_url, await self.mm_id, user_id, channel.id
                )
                return user_id
        raise ValueError("This is not a direct channel", channel)

    async def get_channels(self) -> list[Channel]:
        channels = await self.get_channels_for_user("me")
        log.debug("Channels: %s", channels)

        if not channels:
            # happens on INRIA's matternost, maybe disabled by admin instance?
            channels = []
            for team in await self.get_teams_for_user("me"):
                if not team.id:
                    log.warning("Team without ID")
                    continue

                team_channels = await self.get_channels_for_team_for_user("me", team.id)

                if not team_channels:
                    log.warning("Team without channels")
                    continue

                for channel in team_channels:
                    channels.append(channel)
        return channels

    async def get_contacts(self):
        user_ids = []
        for c in await self.get_channels():
            if c.type != "D":
                continue
            if not c.last_post_at:
                # there is no real notion of "contact" on mattermost,
                # but because we regularly poll contact's statuses, we consider
                # contacts people we already exchanged messages with
                log.debug("Ignoring empty direct channel: %s", c)
                continue
            assert isinstance(c.name, str)
            try:
                user_ids.append(
                    await self.__get_other_user_id_from_direct_channel_name(c)
                )
            except ValueError:
                # note to self
                pass
        return user_ids

    async def send_message_to_user(
        self, username: str, text: str, thread: Optional[str] = None
    ) -> str:
        await self.mm_id

        other = await self.get_user_by_username(username)
        if not other.id:
            raise XMPPError("internal-server-error")
        return await self.send_message_to_user_id(other.id, text, thread)

    async def send_message_to_user_id(
        self, user_id: str, text: str, thread: Optional[str] = None
    ) -> str:
        direct_channel_id = await self.get_direct_channel_id(user_id)
        return await self.send_message_to_channel(direct_channel_id, text, thread)

    async def __send_or_create_thread(
        self, post: CreatePostJsonBody, thread: Optional[str] = None
    ) -> Post:
        post.root_id = thread or UNSET
        try:
            msg = await self.create_post(post)
        except XMPPError as e:
            if e.condition != "bad-request":
                raise
            log.debug("Looks like it's a new thread")
            post.root_id = UNSET
            msg = await self.create_post(post)
        return msg

    async def send_message_to_channel(
        self, channel_id: str, text: str, thread: Optional[str] = None
    ):
        msg = await self.__send_or_create_thread(
            CreatePostJsonBody(channel_id=channel_id, message=text), thread
        )

        if not msg.id:
            # This "never" happens, it's probably just a bad open api schema or
            # the api client generator that mistypes it as possibly unset.
            raise XMPPError("internal-server-error", "The message has no message ID")

        return msg.id

    async def send_message_with_file(self, channel_id: str, file_id: str, thread=None):
        r = await self.__send_or_create_thread(
            CreatePostJsonBody(channel_id=channel_id, file_ids=[file_id], message=""),
            thread,
        )

        return r.id

    async def get_direct_channel_id(self, user_id: str) -> str:
        cached = self._cache.get_direct_channel_id(
            self.base_url, await self.mm_id, user_id
        )
        if cached:
            return cached
        direct_channel = await self.create_direct_channel([await self.mm_id, user_id])
        if not direct_channel or not direct_channel.id:
            raise RuntimeError("Could not create direct channel")
        username = await self.get_username_by_user_id(user_id)
        self._cache.add_user(self.base_url, user_id, username)
        self._cache.add_direct_channel(
            self.base_url, await self.mm_id, user_id, direct_channel.id
        )
        return direct_channel.id

    async def update_post(self, post_id: str, body: str):
        await self._update_post(
            post_id,
            json_body=UpdatePostJsonBody(id=post_id, message=body),
        )

    async def get_latest_post_id_for_channel(
        self, channel_id: str
    ) -> Optional[Union[str, Unset]]:
        cache = self._cache.msg_id_get(await self.mm_id, channel_id)
        if cache is not None:
            return cache

        async for post in self.get_posts_for_channel(channel_id, per_page=1):
            last = post
            break
        else:
            return None
        if post.id:
            self._cache.msg_id_store(await self.mm_id, channel_id, post.id)
        return last.id

    async def get_posts_for_channel(
        self,
        channel_id: str,
        per_page: Optional[int] = 60,
        before: Optional[Union[str, Unset]] = None,
    ) -> AsyncIterator[Post]:
        """
        Returns posts from the most recent to the oldest one

        :param channel_id:
        :param per_page:
        :param before: a msg id, return messages before this one
        :return : posts with decreasing created_at timestamp
        """
        while True:
            post_list = await self._get_posts_for_channel(
                channel_id,
                per_page=per_page,
                before=before,  # , page=page
            )
            posts = post_list.posts
            if not posts:
                break
            if not post_list.order:
                break
            if not posts.additional_properties:
                break
            posts_dict = posts.additional_properties
            for post_id in post_list.order:
                yield posts_dict[post_id]
            before = post_list.prev_post_id
            if not before:
                break

    async def upload_file(
        self, channel_id: str, url: str, http_response: aiohttp.ClientResponse
    ):
        data = await http_response.read()
        req = UploadFileMultipartData(
            files=File(file_name=url.split("/")[-1], payload=io.BytesIO(data)),
            channel_id=channel_id,
        )
        r = await upload_file.asyncio(client=self.http, multipart_data=req)
        if not r or r.file_infos is None or not r.file_infos or len(r.file_infos) != 1:
            raise RuntimeError(r)
        return r.file_infos[0].id

    async def react(self, post_id: str, emoji: str):
        return await self._save_reaction(
            Reaction(
                user_id=await self.mm_id,
                post_id=post_id,
                emoji_name=demojize(emoji),
            )
        )

    async def get_reactions(self, post_id: str) -> set[tuple[str, str]]:
        try:
            r = await self._get_reactions(post_id)
        except TypeError:
            # posts with no reaction trigger
            #   File "/mattermost_api_reference_client/api/reactions/get_reactions.py", line 31, in _parse_response
            #     for response_200_item_data in _response_200:
            # TypeError: 'NoneType' object is not iterable
            # either mattermost-api-client bug or bad openapi schema
            return set()
        return {(x.user_id, emojize_single(x.emoji_name)) for x in r}  # type:ignore

    async def delete_reaction(self, post_id: str, emoji: str):
        emoji_name = demojize(emoji)
        await self._delete_reaction(await self.mm_id, post_id, emoji_name=emoji_name)

    async def view_channel(self, channel_id: str):
        await self._view_channel(
            await self.mm_id, json_body=ViewChannelJsonBody(channel_id=channel_id)
        )

    async def set_user_status(self, status: StatusType, text: Optional[str] = None):
        my_id = await self.mm_id
        await self._update_user_status(
            my_id,
            json_body=UpdateUserStatusJsonBody(user_id=my_id, status=status),
        )
        if text:
            try:
                emo_str = next(emoji.analyze(text, False, True))
            except StopIteration:
                emo_alias = "speech_balloon"
            else:
                emo_alias = demojize(emo_str.chars)
            await self._update_user_custom_status(
                user_id=my_id,
                json_body=UpdateUserCustomStatusJsonBody(emoji=emo_alias, text=text),
            )
        else:
            await unset_user_custom_status.asyncio_detailed(
                user_id=my_id, client=self.http
            )


P = ParamSpec("P")
T = TypeVar("T")


async def call_with_args_or_json_body(
    func: Callable[..., Awaitable[Response[T]]], client, use_json_body: bool, *a, **k
) -> Response[T]:
    if use_json_body:
        json_body = k.pop("json_body", None)
        if not json_body:
            json_body = a[0]
            a = a[1:]
        resp = await func(*a, **k, json_body=json_body, client=client)
    else:
        resp = await func(*a, **k, client=client)
    raise_maybe(resp)
    return resp


def authenticated_call(
    func: Callable[..., Awaitable[Response[T]]],
    client: AuthenticatedClient,
    force_json_decode=False,
    use_json_body=False,
) -> Callable[..., Awaitable[T]]:
    async def wrapped(*a: P.args, **k: P.kwargs):  # type:ignore
        resp = await call_with_args_or_json_body(func, client, use_json_body, *a, **k)
        if force_json_decode:
            return json.loads(resp.content)
        return resp.parsed

    return wrapped


def authenticated_call_return_content(
    func: Callable[..., Awaitable[Response]],
    client: AuthenticatedClient,
    use_json_body=False,
    return_none_when_not_found=False,
) -> Callable[..., Awaitable[bytes]]:
    async def wrapped(*a: P.args, **k: P.kwargs):  # type:ignore
        try:
            resp = await call_with_args_or_json_body(
                func, client, use_json_body, *a, **k
            )
        except XMPPError as e:
            if e.condition == "item-not-found" and return_none_when_not_found:
                return None
            raise
        return resp.content

    return wrapped


def paginated(
    func: Callable[..., Awaitable[list[T]]],
) -> Callable[..., AsyncIterator[T]]:
    @functools.wraps(func)
    async def wrapped(*a, **k):
        page = 0
        while True:
            result = await func(*a, **k, page=page)
            if not result:
                break
            for r in result:
                yield r
            page += 1

    return wrapped


def raise_maybe(resp: Response):
    status = resp.status_code
    if status < 200 or status >= 300:
        raise MattermostException(resp)
    if isinstance(resp.parsed, StatusOK) and (resp.parsed.status or "").lower() != "ok":
        raise XMPPError("internal-server-error", str(resp.parsed.status))


def get_client_from_registration_form(f: dict[str, Optional[str]], cache: Cache):
    url = f["url"].rstrip("/") or ""  # type:ignore
    return MattermostClient(
        url,
        cache,
        verify_ssl=f["strict_ssl"],
        timeout=5,
        token=f["token"],
    )


log = logging.getLogger(__name__)
