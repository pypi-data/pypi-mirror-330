import pytest
from mattermost_api_reference_client.models import Channel, User

from matteridge.events import StatusType
from matteridge.websocket import Websocket, WebsocketRequestError


@pytest.mark.asyncio
async def test_user_typing(ws: Websocket, direct_channel: Channel):
    x = await ws.user_typing(direct_channel.id)
    assert x is None
    await ws.user_typing(direct_channel.id)
    with pytest.raises(WebsocketRequestError):
        await ws.user_typing(123)
    await ws.user_typing(direct_channel.id)


@pytest.mark.asyncio
async def test_get_statuses(ws: Websocket):
    for i in range(3):
        statuses = await ws.get_statuses()
        assert statuses
        for user_id, status in statuses.items():
            assert isinstance(user_id, str)
            assert status in StatusType.__args__


@pytest.mark.asyncio
async def test_get_statuses_by_id(ws: Websocket, contact: User):
    for i in range(3):
        statuses = await ws.get_statuses_by_ids([contact.id])
        assert statuses
        assert contact.id in statuses
        for user_id, status in statuses.items():
            assert isinstance(user_id, str)
            assert status in StatusType.__args__


@pytest.mark.asyncio
async def test_reconnection(ws: Websocket, contact: User):
    statuses = await ws.get_statuses()
    assert statuses
    await ws._ws.close()
    statuses = await ws.get_statuses()
    assert statuses
