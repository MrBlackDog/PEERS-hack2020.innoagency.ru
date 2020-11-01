import asyncio
import logging
import threading
from multiprocessing import Process, Manager
#import task as task
import websockets
#from fly import *
from websockets import WebSocketServerProtocol
logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    def __init__(self, config, web_message_buffer):
        self.config = config
        self.web_message_buffer = web_message_buffer

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        await ws.close(1000, "normal closure")
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def ws_handler(self, ws: WebSocketServerProtocol, url: str) -> None:
        await self.register(ws)
        consumer_task = asyncio.ensure_future(
            self.consumer_handler(ws))
        producer_task = asyncio.ensure_future(
            self.producer_handler(ws))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

    async def consumer_handler(self, websocket):
        async for message in websocket:
            await self.consumer(message)

    async def producer_handler(self, websocket):
        while True:
            message = await self.producer()
            if len(message) > 0:
                await websocket.send(message)

    async def producer(self) -> str:
        await asyncio.sleep(0.001)
        mes = ""
        if len(self.web_message_buffer) > 0:
            mes = self.web_message_buffer.pop(0)
        # for mes in self.web_message_buffer:
        #     returnmes += tag.ID + " "
        #     returnmes += str(tag.x) + " "
        #     returnmes += str(tag.y) + " "
        # print("web " + returnmes)
        return mes

    async def consumer(self, message):
        logging.info(f'{message} connects')

    @staticmethod
    def send_to_all(message):
        ([client.send(message) for client in Server.clients])

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            print(message)
            # (x, y) = fly.getflycoord(myfly)
            # await self.send_to_clients(x + " " + y)
            await self.send_to_clients(message)


#  async def sendflycoord(self, ws: WebSocketServerProtocol) -> None:


# loop.run_forever()

