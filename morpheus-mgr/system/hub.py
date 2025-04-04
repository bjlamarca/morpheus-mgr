import json, traceback, ipaddress, socket, threading
from pathlib import Path
from peewee import PostgresqlDatabase
from system.logger import SystemLogger
from system.signals import Signal

logger = SystemLogger(__name__)


BASE_DIR = str(Path(__file__).resolve().parent.parent)


class HubManger:

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
            cls.connect_db_hub(cls._instance)
                
        return cls._instance

    def __init__(cls):
        pass

    def connect_db_hub(cls, signal_grp=None):
        msg_dict = {}
        try:
            db_serv_dict = cls.get_current_db_hub()
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
            msg_dict['message'] = 'Error connecting to database hub.'
            logger.log('connect_db_hub', msg_dict['message'], str(e) + traceback.format_exc(), 'ERROR') 
            if signal_grp:
                Signal().send(signal_grp, cls, msg_dict)
            return msg_dict
        else:
            cls.db_connected = True
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Connected to database hub.'
            if signal_grp:
                Signal().send(signal_grp, cls, msg_dict)
            logger.log('connect_db_hub', 'Connected to database hub.', 'Database hub: ' + cls.db_host, 'INFO')
            return msg_dict

    def get_hub_list(cls):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        hub_list = settings['hub_list']
        return hub_list

    def set_hub_list(cls, hub_list):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        f.close()
        settings['hub_list'] = hub_list
        f = open(BASE_DIR + '/settings.json', 'w')
        f.write(json.dumps(settings, indent=4))
        f.close()

    def get_hub_info(cls, hub_id):
        hub_list = cls.get_hub_list()
        for hub in hub_list:
            if hub['id'] == hub_id:
                return hub

    def get_current_hub(cls):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        current_hub = settings['current_hub_id']
        hub_list = settings['hub_list']
        for hub in hub_list:
            if hub['id'] == current_hub:
                return hub
            
    def set_current_hub(cls, hub_id):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        settings['current_hub_id'] = hub_id
        f = open(BASE_DIR + '/settings.json', 'w')
        f.write(json.dumps(settings, indent=4))
        f.close()
            
    def get_current_db_hub(cls):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        current_db_hub = settings['current_db_hub_id']
        hub_list = settings['hub_list']
        for hub in hub_list:
            if hub['id'] == current_db_hub:
                return hub
            
    def set_current_db_hub(cls, hub_id):
        msg_dict = {}
        try: 
            f = open(BASE_DIR + '/settings.json', 'r')
            settings = json.load(f)
            settings['current_db_hub_id'] = hub_id
            f = open(BASE_DIR + '/settings.json', 'w')
            f.write(json.dumps(settings, indent=4))
            f.close()
        except Exception as e:
            msg_dict['status'] = 'error'
            msg_dict['message'] = 'Error setting database hub.'
            logger.log('set_current_db_hub', msg_dict['message'], str(e) + traceback.format_exc(), 'ERROR') 
            return msg_dict
        else:
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Database hub set.  Please restart Morpheus.'
            logger.log('set_current_db_hub', 'Database hub set.  Please restart Morpheus.', 'Database hub: ' + str(hub_id), 'INFO')
            return msg_dict

    def add_hub(cls, name, ip_addr):
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
            hub_list = cls.get_hub_list()
            id = 0
            for hub in hub_list:
                if hub['id'] > id:
                    id = hub['id']
            hub = {
                'name': name,
                'ip_addr': ip_addr,
                'id': id + 1
            }
            hub_list.append(hub)
            cls.set_hub_list(hub_list)
            
        except Exception as e:
                    traceback.print_exc()
                    logger.log('add_hub', 'Error adding hub.', str(e) + traceback.format_exc(), 'ERROR')
                    msg_dict['status'] = 'error'
                    msg_dict['message'] = 'Error adding hub.' + str(e)
                    return msg_dict
                
        else:
            logger.log('add_hub', 'hub has been added', 'hub: ' + str(hub), 'INFO')
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'hub has been added successfully.'
            return msg_dict

    def edit_hub(cls, name, ip_addr, hub_id):
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
            hub_list = cls.get_hub_list()
            for hub in hub_list:
                if hub['id'] == hub_id:
                    hub['name'] = name
                    hub['ip_addr'] = ip_addr
                    cls.set_hub_list(hub_list)

        except Exception as e:
                    traceback.print_exc()
                    logger.log('edit_hub', 'Error updating hub.', str(e) + traceback.format_exc(), 'ERROR')
                    msg_dict['status'] = 'error'
                    msg_dict['message'] = 'Error updating hub.' + str(e)
                    return msg_dict
                
        else:
            logger.log('edit_hub', 'hub has been updated', 'hub: ' + str(hub), 'INFO')
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'hub has been updated successfully.'
            return msg_dict

    def delete_hub(cls, hub_id):
        msg_dict = {}
        try:
            hub_list = cls.get_hub_list()
            for hub in hub_list:
                if hub['id'] == hub_id:
                    hub_list.remove(hub)
                    cls.set_hub_list(hub_list)
        except Exception as e:
                    traceback.print_exc()
                    logger.log('edit_hub', 'Error deleting hub.', str(e) + traceback.format_exc(), 'ERROR')
                    msg_dict['status'] = 'error'
                    msg_dict['message'] = 'Error deleting hub.' + str(e)
                    return msg_dict
                
        else:
            logger.log('edit_hub', 'hub has been deleted', 'hub: ' + str(hub), 'INFO')
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'hub has been deleted successfully.'
            return msg_dict
        

class HubSocket:
    _instance = None
    hub_connected = False
    hub_host = ''
    hub_port = 8999
    hub_mrg = HubManger()
    websocket = None
    client = None
    
    def __new__(cls):
        if cls._instance is None:
            print('Creating new instance of hub socket')
            cls._instance = super().__new__(cls)
            cls.hub_host = cls.hub_mrg.get_current_hub()['ip_addr']
           
        return cls._instance
    
    def __init__(cls):
        pass

    def connect_socket(cls):

        cls.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.client.connect((cls.hub_host, cls.hub_port))
        
    def send(cls, message):
        if cls.client:
            msg = message.encode('utf-8')
            msg_length = len(msg)
            send_length = str(msg_length).encode('utf-8')
            send_length += b' ' * (256 - len(send_length))
            cls.client.send(send_length)
            cls.client.send(msg)
    

      