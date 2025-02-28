from datetime import datetime
from typing import TYPE_CHECKING, Awaitable, Callable, TypeVar, Union

import emoji as emoji_lib
from mattermost_api_reference_client.models import FileInfo
from mattermost_api_reference_client.types import Unset
from slidge.core.mixins.message import ContentMessageMixin
from slidge.util.types import LegacyAttachment

from .events import Post

if TYPE_CHECKING:
    from .session import Session


def _emoji_name_conversion(x: str):
    return (
        x.replace("_3_", "_three_")
        .replace("thumbsup", "+1")
        .replace("star_struck", "star-struck")
    )


def emojize_single(x: str, add_delimiters=True):
    if add_delimiters:
        x = f":{x}:"
    char = emoji_lib.emojize(f"{_emoji_name_conversion(x)}", language="alias")
    if not emoji_lib.is_emoji(char):
        return "❓"
    return char


def emojize_body(body: str):
    char = emoji_lib.emojize(f"{_emoji_name_conversion(body)}", language="alias")
    return char


def demojize(emoji_char: str):
    return _emoji_name_conversion(
        emoji_lib.demojize(emoji_char, delimiters=("", ""), language="alias")
    )


class UserMixin(ContentMessageMixin):
    session: "Session"
    mm_id: Callable[[], Awaitable[str]]

    async def send_mm_post(self, post: Post, carbon=False, archive_only=False):
        assert post.metadata
        assert post.update_at

        file_metas = post.metadata.files
        if not (isinstance(file_metas, list)):
            file_metas = []
        if isinstance(m := post.message, str):
            text = emojize_body(m)
        else:
            text = ""
        post_id = post.id

        when = datetime.fromtimestamp(post.update_at / 1000)

        await self.send_files(
            [
                Attachment.from_mm(x, await self.session.mm_client.get_file(x.id))
                for x in file_metas
            ],
            post_id,
            body=text,
            when=when,
            carbon=carbon,
            thread=post.root_id or post_id,
            body_first=True,
            archive_only=archive_only,
        )

    async def update_reactions(self, legacy_msg_id: str, carbon: bool = False):
        self.react(
            legacy_msg_id,
            await self.session.get_mm_reactions(
                legacy_msg_id,
                await self.session.mm_client.mm_id if carbon else await self.mm_id(),
            ),
            carbon=carbon,
        )


class Attachment(LegacyAttachment):
    @staticmethod
    def from_mm(info: FileInfo, data: bytes):
        return Attachment(
            name=unset_to_none(info.name),
            legacy_file_id=unset_to_none(info.id),
            # TODO: data could be an awaitable of bytes in slidge core so we don't
            #       have to fetch if legacy_file_id has already been seen
            data=data,
        )


T = TypeVar("T")


def unset_to_none(x: Union[T, Unset]) -> Union[T, None]:
    if isinstance(x, Unset):
        return None
    return x
