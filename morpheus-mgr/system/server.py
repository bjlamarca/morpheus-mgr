import json, traceback
from pathlib import Path
import asyncio
from websockets.asyncio.client import connect
from system.logging import SystemLogger
from system.signals import Signal

logger = SystemLogger(__name__)
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


class ServerManger:
    def __init__(self):
        pass

    def get_server_list(self):
        f = open(BASE_DIR + '\settings.json', 'r')
        settings = json.load(f)
        server_list = settings['server_connect_list']
        return server_list
    
    def set_server_settings(self, server_list, signal_grp=None):
        msg_dict = {'status': 'start', 'message': 'Setting server list'}
        if signal_grp:
            signal = Signal()
            signal.send(signal_grp, 'set_server_settings', msg_dict)
        try:
            f = open('settings.json', 'r')
            settings = json.load(f)
            f.close()
            settings['server_connect_list'] = server_list
            f = open('settings.json', 'w')
            f.write(json.dumps(settings))
            f.close()
        except Exception as e:
            traceback.print_exc()
            logger.log('sync_device_types', 'Error syncing device types.', str(e) + traceback.format_exc(), 'ERROR')
            msg_dict['status'] = 'error'
            msg_dict['message'] = 'Error syncing device types. ' + str(e)
            if signal_grp:
                signal.send(signal_grp, 'sync_device_types', msg_dict)
            return msg_dict
        
        else:
            logger.log('sync_device_types', 'Device types synced.', 'Device types synced successfully.', 'INFO')
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Device types synced successfully.'
            if signal_grp:
                signal.send(signal_grp, 'sync_device_types', msg_dict)
            return msg_dict


    def get_server(self, server_id):
        server_list = self.get_server_list()
        for server in server_list:
            if server['id'] == server_id:
                return server

    def add_server(self, server):
        server_list = self.get_server_list()
        server_list.append(server)
        self.set_server_settings(server_list)

    def edit_server(self, server):
        server_list = self.get_server_list()


    def delete_server(self, server_id):
        server_list = self.get_server_list()
        for server in server_list:
            if server['id'] == server_id:
                server_list.remove(server)
                self.set_server_settings(server_list)
                return {'status': 'success', 'message': 'Server deleted'}
        return {'status': 'error', 'message': 'Server not found'}