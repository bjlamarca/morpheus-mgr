import sys, json
from pathlib import Path
import asyncio
from websockets.asyncio.client import connect

BASE_DIR = str(Path(__file__).resolve().parent.parent)

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


class ServerConnection:
    def __init__(self):
        pass

    def get_server_list(self):
        f = open(BASE_DIR + 'settings.json', 'r')
        settings = json.load(f)
        server_list = settings['server_connect_list']
        return server_list
    
    def set_server_settings(self, server_list):
        f = open('settings.json', 'r')
        settings = json.load(f)
        f.close()
        settings['server_connect_list'] = server_list
        f = open('settings.json', 'w')
        f.write(json.dumps(settings))
        f.close()