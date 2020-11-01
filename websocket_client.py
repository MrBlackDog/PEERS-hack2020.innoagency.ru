# PEERS RTLS Platform
# Copyright (C) NEELAR LLC, 2020
# business@neelar.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import asyncio
import logging
import threading

import websockets
from websockets import WebSocketServerProtocol
#import matplotlib
import logsreader
logging.basicConfig(level=logging.INFO)
SERVER = '192.168.43.196'
PORT = "5050"


class Web_client():

    def __init__(self, ipaddres, port):
        self.ipaddr = ipaddres
        self.port = port
        self.websocket_resourse_url = f"ws://{SERVER}:{PORT}/web"

    async def handler(self, websocket: WebSocketServerProtocol) -> None:
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

    async def consumer(self, message):
        await asyncio.sleep(0.0001)
        gui.web_message_buffer.append(message)
        # await gui.drawframe(message)
        #self.log_message(message)

    async def producer_handler(self,websocket: WebSocketServerProtocol):
        while True:
            await asyncio.sleep(0.0001)
            message = await self.producer()
            # await websocket.send(message)

    async def producer(self):
       await asyncio.sleep(0.0001)

    def log_message(self,message: str) -> None:
        logging.info(f"Message:{message}")

    async def connect(self):
        async with websockets.connect(self.websocket_resourse_url) as ws:
            await self.handler(ws)


def asyncio_thread(async_loop):
    async_loop.run_until_complete(client.connect())


if __name__ == '__main__':
    gui = logsreader.peers_gui()
    client = Web_client("192.168.0.174", "5050")
    loop = asyncio.get_event_loop()
    threading.Thread(target=asyncio_thread, args=(loop,)).start()
    # loop.run_until_complete(client.connect())
    # gui.tk.update()
    # loop.create_task(gui.tk.mainloop())
    # loop.create_task()
    gui.tk.mainloop()
    # loop.run_forever()

