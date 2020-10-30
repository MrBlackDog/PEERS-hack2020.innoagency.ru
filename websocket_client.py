import asyncio
import logging
import websockets
from websockets import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)
SERVER = '192.168.0.174'
PORT = "5050"


class Websocket_client():

    def __init__(self, ipaddres, port):
        self.ipaddr = ipaddres
        self.port = port
        self.websocket_resourse_url = f"ws://{SERVER}:{PORT}/web"

    async def handler(self,websocket: WebSocketServerProtocol) -> None:
        consumer_task = asyncio.ensure_future(
            self.consumer_handler(websocket))
        producer_task = asyncio.ensure_future(
            self.producer_handler(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()


    async def consumer_handler(self,websocket: WebSocketServerProtocol):
        async for message in websocket:
            await self.consumer(message)


    async def consumer(self,message):
        self.log_message(message)


    async def producer_handler(self,websocket: WebSocketServerProtocol):
        while True:
            message = await self.producer()
            await websocket.send(message)


    async def producer(self) -> str:
        return input()


    def log_message(self,message: str) -> None:
        logging.info(f"Message:{message}")


    async def connect(self):
        async with websockets.connect(self.websocket_resourse_url) as ws:
            await self.handler(ws)


if __name__ == '__main__':
    client = Websocket_client("192.168.0.33", "5050")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.connect())
    loop.run_forever()
