import unittest.mock
import uuid
import shutil
from subprocess import check_output, CalledProcessError
from time import sleep

import aiohttp
import pytest
import pytest_asyncio
from mattermost_api_reference_client.models import User

from matteridge.api import MattermostClient
from matteridge.cache import Cache
from matteridge.websocket import Websocket

HOST = "http://localhost:8066"

PODMAN_BIN = shutil.which("docker") or shutil.which("podman")

if PODMAN_BIN is None:
    print("Podman or docker executables not found, cannot run MM integration tests")

def launch_container():
    check_output(
        [
            PODMAN_BIN,
            "run",
            "--rm",
            "--name",
            "matteridge-tests",
            "-d",
            "--publish",
            "127.0.0.1:8066:8065",
            "--add-host",
            "dockerhost:127.0.0.1",
            "--env",
            "MM_SERVICESETTINGS_ENABLELOCALMODE=1",
            "docker.io/mattermost/mattermost-preview",
        ]
    )


@pytest.fixture(scope="session")
def start_docker():
    try:
        check_output([PODMAN_BIN, "container", "inspect", "matteridge-tests"])
    except CalledProcessError as e:
        print(f"Creating test container {e}, {e.output}")
        launch_container()
        was_there_before = False
    else:
        was_there_before = True
        print("Test container already running")
    yield
    if was_there_before:
        return
    # we only stop it if it wasn't running before, so that it's possible
    # to spin it up manually and not need to bring it up again every time
    # we want to run tests, during dev
    check_output([PODMAN_BIN, "stop", "matteridge-tests"])


def mmctl(*args, fatal=True):
    try:
        return check_output(
            [PODMAN_BIN, "exec", "matteridge-tests", "mmctl", "--local", *args]
        )
    except CalledProcessError as e:
        print(e)
        if fatal:
            raise


def create_user(username):
    mmctl(
        "user",
        "create",
        "--email",
        f"{uuid.uuid4()}@slidge.im",
        "--username",
        username,
        "--password",
        "test12345",
        "--system-admin",
        fatal=False,
    )
    mmctl("team", "users", "add", "test-team", username, fatal=False)


@pytest.fixture(scope="module")
def matteridge_test_container(start_docker):
    exc = CalledProcessError
    for i in range(60):
        try:
            mmctl("user", "list")
        except CalledProcessError as e:
            exc = e
            print(i, e)
            sleep(1)
        else:
            break
    else:
        raise exc
    mmctl("team", "create", "--name=test-team", "--display-name=Test-team", fatal=False)
    mmctl(
        "channel",
        "create",
        "--team=test-team",
        "--name=test-channel",
        "--display-name='Test channel'",
        fatal=False,
    )
    create_user("test")
    create_user("test2")


@pytest_asyncio.fixture
async def token(matteridge_test_container):
    return await MattermostClient.get_token(HOST, "test", "test12345")


@pytest_asyncio.fixture
async def mm(token, tmp_path):
    cache = Cache(tmp_path / "test.sql")
    client = MattermostClient(HOST, cache, token=token, verify_ssl=False)
    await client.login()
    await client.send_message_to_user("test2", "We are now contacts, motherfucker!")
    return client


@pytest_asyncio.fixture
async def contact(mm: MattermostClient):
    user_ids = await mm.get_contacts()
    user_id = user_ids[0]
    return await mm.get_user(user_id)


@pytest_asyncio.fixture
async def direct_channel(mm: MattermostClient, contact: User):
    return await mm.get_channel(await mm.get_direct_channel_id(contact.id))


@pytest_asyncio.fixture
async def ws_non_connected(mm, token, matteridge_test_container):
    async with aiohttp.ClientSession() as session:
        w = Websocket(HOST + "/api/v4/websocket", token, session)
        yield w


@pytest_asyncio.fixture
async def ws(ws_non_connected, event_loop):
    handler = unittest.mock.AsyncMock()
    task = event_loop.create_task(ws_non_connected.connect(handler))
    ws_non_connected.event_handler = handler
    yield ws_non_connected
    await ws_non_connected._ws.close()
    task.cancel()


if __name__ == "__main__":
    launch_container()
