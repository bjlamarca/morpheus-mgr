import json, traceback, ipaddress, socket, threading
from pathlib import Path
from peewee import PostgresqlDatabase
from system.logger import SystemLogger
from system.signals import Signal

logger = SystemLogger(__name__)


BASE_DIR = str(Path(__file__).resolve().parent.parent)


class ServerManger:

    _instance = None
    db_connected = False
    db = None
    db_name = 'morpheus2'
    db_host = ''
    db_port = 5432
    db_user = 'morpheus'
    db_password = 'Buster77!'
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.connect_db_server(cls._instance)
                
        return cls._instance

    def __init__(cls):
        pass

    def connect_db_server(cls, signal_grp=None):
        msg_dict = {}
        try:
            db_serv_dict = cls.get_current_db_server()
            cls.db_host = db_serv_dict['ip_addr']
            cls.db = PostgresqlDatabase(cls.db_name, host=cls.db_host, port=cls.db_port, user=cls.db_user,
                password=cls.db_password)
            #run a test query to see if connection is successful
            from system.models import Room
            test_qs = Room.select()
        except Exception as e:
            traceback.print_exc()
            cls.db_connected = False
            msg_dict['status'] = 'error'
            msg_dict['message'] = 'Error connecting to database server.'
            logger.log('connect_db_server', msg_dict['message'], str(e) + traceback.format_exc(), 'ERROR') 
            if signal_grp:
                Signal().send(signal_grp, cls, msg_dict)
            return msg_dict
        else:
            cls.db_connected = True
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Connected to database server.'
            if signal_grp:
                Signal().send(signal_grp, cls, msg_dict)
            logger.log('connect_db_server', 'Connected to database server.', 'Database server: ' + cls.db_host, 'INFO')
            return msg_dict

    def get_server_list(cls):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        server_list = settings['server_list']
        return server_list

    def set_server_list(cls, server_list):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        f.close()
        settings['server_list'] = server_list
        f = open(BASE_DIR + '/settings.json', 'w')
        f.write(json.dumps(settings, indent=4))
        f.close()

    def get_server_info(cls, server_id):
        server_list = cls.get_server_list()
        for server in server_list:
            if server['id'] == server_id:
                return server

    def get_current_server(cls):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        current_server = settings['current_server_id']
        server_list = settings['server_list']
        for server in server_list:
            if server['id'] == current_server:
                return server
            
    def set_current_server(cls, server_id):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        settings['current_server_id'] = server_id
        f = open(BASE_DIR + '/settings.json', 'w')
        f.write(json.dumps(settings, indent=4))
        f.close()
            
    def get_current_db_server(cls):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        current_db_server = settings['current_db_server_id']
        server_list = settings['server_list']
        for server in server_list:
            if server['id'] == current_db_server:
                return server
            
    def set_current_db_server(cls, server_id):
        msg_dict = {}
        try: 
            f = open(BASE_DIR + '/settings.json', 'r')
            settings = json.load(f)
            settings['current_db_server_id'] = server_id
            f = open(BASE_DIR + '/settings.json', 'w')
            f.write(json.dumps(settings, indent=4))
            f.close()
        except Exception as e:
            msg_dict['status'] = 'error'
            msg_dict['message'] = 'Error setting database server.'
            logger.log('set_current_db_server', msg_dict['message'], str(e) + traceback.format_exc(), 'ERROR') 
            return msg_dict
        else:
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Database server set.  Please restart Morpheus.'
            logger.log('set_current_db_server', 'Database server set.  Please restart Morpheus.', 'Database server: ' + str(server_id), 'INFO')
            return msg_dict

    def add_server(cls, name, ip_addr):
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
            server_list = cls.get_server_list()
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
            cls.set_server_list(server_list)
            
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

    def edit_server(cls, name, ip_addr, server_id):
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
            server_list = cls.get_server_list()
            for server in server_list:
                if server['id'] == server_id:
                    server['name'] = name
                    server['ip_addr'] = ip_addr
                    cls.set_server_list(server_list)

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

    def delete_server(cls, server_id):
        msg_dict = {}
        try:
            server_list = cls.get_server_list()
            for server in server_list:
                if server['id'] == server_id:
                    server_list.remove(server)
                    cls.set_server_list(server_list)
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
        

class ServerSocket:
    _instance = None
    server_connected = False
    server_host = ''
    server_port = 8999
    server_mrg = ServerManger()
    websocket = None
    client = None
    
    def __new__(cls):
        if cls._instance is None:
            print('Creating new instance of ServerWebsocket')
            cls._instance = super().__new__(cls)
            cls.server_host = cls.server_mrg.get_current_server()['ip_addr']
           
        return cls._instance
    
    def __init__(cls):
        pass

    def connect_socket(cls):

        cls.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.client.connect((cls.server_host, cls.server_port))
        
    def send(cls, message):
        if cls.client:
            msg = message.encode('utf-8')
            msg_length = len(msg)
            send_length = str(msg_length).encode('utf-8')
            send_length += b' ' * (256 - len(send_length))
            cls.client.send(send_length)
            cls.client.send(msg)
    

      