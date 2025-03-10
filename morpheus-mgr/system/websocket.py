import asyncio
from websockets.asyncio.client import connect


async def connect_to_websocket(url):
    async with connect(url) as websocket:
        while True:
            message = await websocket.recv()
            print(message)

async def send():
    async with connect('ws://192.168.55.235:8001') as websocket:
        await websocket.send('hello')


def webs_test():
    asyncio.run(send())