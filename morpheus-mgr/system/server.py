import json, traceback, ipaddress
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
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        server_list = settings['server_list']
        return server_list
    
    def set_server_list(self, server_list):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        f.close()
        settings['server_list'] = server_list
        f = open(BASE_DIR + '/settings.json', 'w')
        f.write(json.dumps(settings, indent=4))
        f.close()

    def get_server_info(self, server_id):
        server_list = self.get_server_list()
        for server in server_list:
            if server['id'] == server_id:
                return server

    def get_current_server(self):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        current_server = settings['current_server_id']
        server_list = settings['server_list']
        for server in server_list:
            if server['id'] == current_server:
                return server
            
    def get_current_db_server(self):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        current_db_server = settings['current_db_server_id']
        server_list = settings['server_list']
        for server in server_list:
            if server['id'] == current_db_server:
                return server

    def add_server(self, name, ip_addr):
        msg_dict = {}
        try:
            if name == '' or ip_addr == '':
                msg_dict['status'] = 'error'
                msg_dict['message'] = 'Name and IP Address are required.'
                return msg_dict
            try:
                ip = ipaddress.ip_address(ip_addr)
            except:
                msg_dict['status'] = 'error'
                msg_dict['message'] = 'Invalid IP Address.'
                return msg_dict
            server_list = self.get_server_list()
            id = 0
            for server in server_list:
                if server['id'] > id:
                    id = server['id']
            server = {
                'name': name,
                'ip_addr': ip_addr,
                'id': id + 1
            }
            server_list.append(server)
            self.set_server_list(server_list)
            print('Server list:', server_list)
        except Exception as e:
                    traceback.print_exc()
                    logger.log('add_server', 'Error adding server.', str(e) + traceback.format_exc(), 'ERROR')
                    msg_dict['status'] = 'error'
                    msg_dict['message'] = 'Error adding server.' + str(e)
                    return msg_dict
                
        else:
            logger.log('add_server', 'Server has been added', 'Server: ' + str(server), 'INFO')
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Server has been added successfully.'
            return msg_dict

    def edit_server(self, name, ip_addr, server_id):
        msg_dict = {}
        try:
            if name == '' or ip_addr == '':
                msg_dict['status'] = 'error'
                msg_dict['message'] = 'Name and IP Address are required.'
                return msg_dict
            try:
                ip = ipaddress.ip_address(ip_addr)
            except:
                msg_dict['status'] = 'error'
                msg_dict['message'] = 'Invalid IP Address.'
                return msg_dict
            server_list = self.get_server_list()
            for server in server_list:
                if server['id'] == server_id:
                    server['name'] = name
                    server['ip_addr'] = ip_addr
                    self.set_server_list(server_list)

        except Exception as e:
                    traceback.print_exc()
                    logger.log('edit_server', 'Error updating server.', str(e) + traceback.format_exc(), 'ERROR')
                    msg_dict['status'] = 'error'
                    msg_dict['message'] = 'Error updating server.' + str(e)
                    return msg_dict
                
        else:
            logger.log('edit_server', 'Server has been updated', 'Server: ' + str(server), 'INFO')
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Server has been updated successfully.'
            return msg_dict

    def delete_server(self, server_id):
        msg_dict = {}
        try:
            server_list = self.get_server_list()
            for server in server_list:
                if server['id'] == server_id:
                    server_list.remove(server)
                    self.set_server_list(server_list)
        except Exception as e:
                    traceback.print_exc()
                    logger.log('edit_server', 'Error deleting server.', str(e) + traceback.format_exc(), 'ERROR')
                    msg_dict['status'] = 'error'
                    msg_dict['message'] = 'Error deleting server.' + str(e)
                    return msg_dict
                
        else:
            logger.log('edit_server', 'Server has been deleted', 'Server: ' + str(server), 'INFO')
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Server has been deleted successfully.'
            return msg_dict