import asyncio
import logging
import ssl
from typing import Optional

import aiohttp

from .events import StatusType, from_dict


class WebsocketRequestError(Exception):
    pass


class Websocket:
    SSL_VERIFY = True
    HEART_BEAT = 30
    MIN_RETRY_TIME = 3
    MAX_RETRY_TIME = 300
    REQUEST_TIMEOUT = 30

    def __init__(self, url, token, client: aiohttp.ClientSession):
        self.token = token
        self.url = url

        self._connected = False
        self._connecting = asyncio.Condition()
        self._ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self._futures: dict[int, asyncio.Future[dict]] = {}
        self._seq_cursor = 1

        self._aiohttp_client = client
        self._attempts = 0

        context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
        if not self.SSL_VERIFY:
            context.verify_mode = ssl.CERT_NONE
        context.load_default_certs()
        self.__context = context

    async def connect(self, event_handler):
        """
        Connect to the websocket and authenticate it.
        When the authentication has finished, start the loop listening for messages,
        sending a ping to the server to keep the connection alive.
        :param event_handler: Every websocket event will be passed there. Takes one argument.
        :type event_handler: Function(message)
        """
        sleep = self.MIN_RETRY_TIME
        while True:
            try:
                await self._connect(event_handler)
            except Exception as e:
                log.error("Error in web socket connection", exc_info=e)
            self._connected = False
            log.info("Web socket connection lost, retrying in %s seconds", sleep)
            await asyncio.sleep(sleep)
            self._attempts += 1
            sleep = min(self._attempts * self.MIN_RETRY_TIME, self.MAX_RETRY_TIME)

    async def _connect(self, event_handler):
        url = self.url
        async with self._aiohttp_client.ws_connect(
            url, ssl=self.__context, heartbeat=self.HEART_BEAT
        ) as ws:
            async with self._connecting:
                await self._initial_connect_sequence(ws)
                self._ws = ws
                self._connected = True
                self._connecting.notify_all()
            self._attempts = 0
            await self.listen(ws, event_handler)
        self._connected = False

    async def _initial_connect_sequence(self, ws: aiohttp.ClientWebSocketResponse):
        self._seq_cursor = 1
        await ws.send_json(
            {
                "seq": self._seq_cursor,
                "action": "authentication_challenge",
                "data": {"token": self.token},
            }
        )

        ok_or_hello = await ws.receive_json()
        if ok_or_hello.get("status") == "OK":
            # the MM docs states that we should receive a OK before the hello,
            # but this does not seem to happen
            hello = await ws.receive_json()
        else:
            hello = ok_or_hello
        if hello["event"] != "hello":
            raise RuntimeError("No Hello from MM server", hello)

        await ws.ping()
        pong = await ws.receive()
        # apparently this triggers the OK?
        log.debug("Pong: %s", pong)

    async def listen(self, ws: aiohttp.ClientWebSocketResponse, event_handler):
        async for msg in ws:
            payload = msg.json()
            log.debug("WS-RECEIVE: %s", payload)
            seq = payload.get("seq_reply")
            if seq is None:
                await event_handler(from_dict(payload))
                continue

            fut = self._futures.pop(seq, None)
            if fut is None:
                log.warning("Ignored an event: %s", payload)
                continue

            fut.set_result(payload)

    async def __request(self, action: str, data: Optional[dict] = None):
        if not self._connected or self._ws and self._ws.closed:
            async with self._connecting:
                await self._connecting.wait()
        assert self._ws is not None
        self._seq_cursor += 1
        seq = self._seq_cursor
        f = self._futures[seq] = asyncio.get_event_loop().create_future()
        req = {"seq": seq, "action": action}
        if data is not None:
            req["data"] = data
        log.debug("WS-SEND: %s", req)
        await self._ws.send_json(req)
        resp = await asyncio.wait_for(f, self.REQUEST_TIMEOUT)
        if resp.get("status") != "OK":
            error_id = resp.get("error", {}).get("id")
            if error_id == "api.web_socket_router.not_authenticated.app_error":
                await self._ws.close()
            elif error_id == "api.context.session_expired.app_error":
                await self._ws.close()
            log.warning("Received a non-OK response: %s", resp)
            raise WebsocketRequestError(resp)
        return resp.get("data")

    async def user_typing(self, channel_id):
        return await self.__request("user_typing", {"channel_id": channel_id})

    async def get_statuses(self) -> dict[str, StatusType]:
        """
        :return: A dict mapping user_ids to statuses
        """
        return await self.__request("get_statuses")

    async def get_statuses_by_ids(self, ids: list[str]) -> dict[str, StatusType]:
        """
        :return: A dict mapping user_ids to statuses
        """
        return await self.__request("get_statuses_by_ids", {"user_ids": ids})


log = logging.getLogger(__name__)
