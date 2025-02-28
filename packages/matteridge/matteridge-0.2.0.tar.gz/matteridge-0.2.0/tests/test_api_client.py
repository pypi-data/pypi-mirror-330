import pytest

from slixmpp.exceptions import XMPPError

from mattermost_api_reference_client.models import (
    Team,
    Channel,
    Status,
    ChannelMember,
    User,
    Post,
)
from matteridge.api import MattermostClient


@pytest.mark.asyncio
async def test_login(mm: MattermostClient):
    me = await mm.get_user("me")
    assert me is not None
    assert me == await mm.me
    assert me.id == await mm.mm_id
    with pytest.raises(expected_exception=XMPPError) as e:
        user = await mm.get_user(1)
        print(user)
    assert e.value.condition == "bad-request"


@pytest.mark.asyncio
async def test_get_teams(mm: MattermostClient):
    teams = await mm.get_teams_for_user("me")
    assert teams
    for t in teams:
        assert isinstance(t, Team)


@pytest.mark.asyncio
async def test_get_users_by_id(mm: MattermostClient, contact: User):
    users = await mm.get_users_by_ids([contact.id])
    assert users[0] == contact


@pytest.mark.asyncio
async def test_get_channels(mm: MattermostClient):
    channels = await mm.get_channels()
    assert channels
    for c in channels:
        assert isinstance(c, Channel)


@pytest.mark.asyncio
async def test_get_contacts(mm: MattermostClient):
    contacts = await mm.get_contacts()
    assert contacts
    for c in contacts:
        assert isinstance(c, str)


@pytest.mark.asyncio
async def test_send_message_to_user(mm: MattermostClient, contact: User):
    msg_id = await mm.send_message_to_user(contact.username, "some-text")
    assert isinstance(msg_id, str)
    channel_id = await mm.get_direct_channel_id(contact.id)
    assert await mm.get_latest_post_id_for_channel(channel_id) == msg_id
    await mm.update_post(msg_id, "some-other-text")


@pytest.mark.asyncio
async def test_get_direct_channel_id(mm: MattermostClient, contact: User):
    channel_id = await mm.get_direct_channel_id(contact.id)
    assert isinstance(channel_id, str)


@pytest.mark.asyncio
async def test_get_profile_image(mm: MattermostClient, contact: User):
    img = await mm.get_profile_image(contact.id)
    assert img
    assert isinstance(img, bytes)


@pytest.mark.asyncio
async def test_get_user_status(mm: MattermostClient, contact: User):
    status = await mm.get_user_status(contact.id)
    assert status
    assert isinstance(status, Status)


@pytest.mark.asyncio
async def test_get_channel_members(mm: MattermostClient):
    channels = await mm.get_channels()
    for c in channels:
        async for member in mm.get_channel_members(c.id):
            assert isinstance(member, ChannelMember)


@pytest.mark.asyncio
async def test_get_posts_for_channel(mm: MattermostClient, contact: User):
    for i in range(10):
        await mm.send_message_to_user_id(contact.id, f"Test{i}")
    channels = await mm.get_channels()
    for c in channels:
        prev = None
        i = 0
        async for post in mm.get_posts_for_channel(c.id, per_page=5):
            assert isinstance(post, Post)
            i += 1
            if prev:
                assert post.create_at < prev
            prev = post.create_at
            if i > 10:
                break


@pytest.mark.asyncio
async def test_start_new_thread(mm: MattermostClient, contact: User):
    await mm.send_message_to_user(contact.username, "Hoy", "random-thread")


@pytest.mark.asyncio
async def test_get_team_icon(mm: MattermostClient):
    team = await mm.get_team_by_name("test-team")
    icon = await mm.get_team_icon(team.id)
    assert isinstance(icon, bytes) or icon is None
