import json
from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional

from mattermost_api_reference_client.models import Post as BasePost
from mattermost_api_reference_client.models import Reaction as BaseReaction
from mattermost_api_reference_client.models import User as BaseUser

ChannelType = Literal["D", "P", "G", "O"]
StatusType = Literal["away", "offline", "online", "dnd"]


# a lot of fields are type-hinted as possibly Unset when they cannot be,
# so these overrides are here as a workaround
class Post(BasePost):
    channel_id: str
    user_id: str
    id: str


class Reaction(BaseReaction):
    user_id: str
    post_id: str


class User(BaseUser):
    username: str


class EventType(str, Enum):
    AddedToTeam = "added_to_team"
    AuthenticationChallenge = "authentication_challenge"
    ChannelConverted = "channel_converted"
    ChannelCreated = "channel_created"
    ChannelDeleted = "channel_deleted"
    ChannelMemberUpdated = "channel_member_updated"
    ChannelUpdated = "channel_updated"
    ChannelViewed = "channel_viewed"
    ConfigChanged = "config_changed"
    DeleteTeam = "delete_team"
    DirectAdded = "direct_added"
    EmojiAdded = "emoji_added"
    EphemeralMessage = "ephemeral_message"
    GroupAdded = "group_added"
    Hello = "hello"
    LeaveTeam = "leave_team"
    LicenseChanged = "license_changed"
    MemberroleUpdated = "memberrole_updated"
    NewUser = "new_user"
    PluginDisabled = "plugin_disabled"
    PluginEnabled = "plugin_enabled"
    PluginStatusesChanged = "plugin_statuses_changed"
    PostDeleted = "post_deleted"
    PostEdited = "post_edited"
    PostUnread = "post_unread"
    Posted = "posted"
    PreferenceChanged = "preference_changed"
    PreferencesChanged = "preferences_changed"
    PreferencesDeleted = "preferences_deleted"
    ReactionAdded = "reaction_added"
    ReactionRemoved = "reaction_removed"
    Response = "response"
    RoleUpdated = "role_updated"
    StatusChange = "status_change"
    Typing = "typing"
    UpdateTeam = "update_team"
    UserAdded = "user_added"
    UserRemoved = "user_removed"
    UserRoleUpdated = "user_role_updated"
    UserUpdated = "user_updated"
    DialogOpened = "dialog_opened"
    ThreadUpdated = "thread_updated"
    ThreadFollowChanged = "thread_follow_changed"
    ThreadReadChanged = "thread_read_changed"

    # not in the https://api.mattermost.com
    SidebarCategoryUpdated = "sidebar_category_updated"

    Unknown = "__unknown__"


@dataclass
class Broadcast:
    channel_id: str
    team_id: str


@dataclass
class MattermostEvent:
    type: EventType
    _data: dict
    _broadcast_dict: dict

    def __post_init__(self):
        self.broadcast = Broadcast(
            self._broadcast_dict["channel_id"], self._broadcast_dict["team_id"]
        )
        self._parse_data(self._data)

    def _parse_data(self, data: dict):
        pass


@dataclass
class Typing(MattermostEvent):
    def _parse_data(self, data: dict):
        self.user_id: str = data["user_id"]


@dataclass
class Posted(MattermostEvent):
    def _parse_data(self, data: dict):
        self.post = Post.from_dict(data["post"])
        self.channel_type: ChannelType = data["channel_type"]
        self.set_online = data.get("set_online", False)


@dataclass
class ChannelViewed(MattermostEvent):
    def _parse_data(self, data: dict):
        self.channel_id: str = data["channel_id"]


@dataclass
class UserUpdated(MattermostEvent):
    def _parse_data(self, data: dict):
        self.user = User.from_dict(data["user"])
        props = self.user.props
        if not props:
            return


class StatusChange(MattermostEvent):
    def _parse_data(self, data: dict):
        self.user_id: str = data["user_id"]
        self.status: StatusType = data["status"]


@dataclass
class PostEdited(MattermostEvent):
    def _parse_data(self, data: dict):
        self.post = Post.from_dict(data["post"])


@dataclass
class PostDeleted(MattermostEvent):
    def _parse_data(self, data: dict):
        self.post = Post.from_dict(data["post"])
        self.delete_by: Optional[str] = data.get("delete_by")


@dataclass
class ReactionAdded(MattermostEvent):
    def _parse_data(self, data: dict):
        self.reaction = Reaction.from_dict(data["reaction"])


@dataclass
class ReactionRemoved(MattermostEvent):
    def _parse_data(self, data: dict):
        self.reaction = Reaction.from_dict(data["reaction"])


@dataclass
class DirectAdded(MattermostEvent):
    def _parse_data(self, data: dict):
        self.creator_id: str = data["creator_id"]
        self.teammate_id: str = data["teammate_id"]


class ChannelCreated(MattermostEvent):
    def _parse_data(self, data: dict):
        self.channel_id: str = data["channel_id"]
        self.team_id: str = data["team_id"]


class UserAdded(MattermostEvent):
    def _parse_data(self, data: dict):
        self.team_id: str = data["team_id"]
        self.user_id: str = data["user_id"]


def from_dict(d) -> MattermostEvent:
    raw_data = d.pop("data")
    data = {}

    for k, v in raw_data.items():
        try:
            # mattermost use single quotes for nested JSON objects, WTF
            data[k] = json.loads(v)
        except (json.JSONDecodeError, TypeError):
            data[k] = v

    bro = d.pop("broadcast")

    try:
        _type = EventType(d.pop("event"))
    except ValueError:
        _type = EventType.Unknown

    cls = _parsed_events.get(str(_type).removeprefix("EventType."), MattermostEvent)
    return cls(_type, data, bro)


_parsed_events = {cls.__name__: cls for cls in MattermostEvent.__subclasses__()}
