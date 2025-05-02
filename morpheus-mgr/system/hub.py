import json, traceback, ipaddress, socket, threading, time
from pathlib import Path
from peewee import PostgresqlDatabase
from system.logger import SystemLogger
from system.signals import Signal
import uuid

logger = SystemLogger(__name__)


BASE_DIR = str(Path(__file__).resolve().parent.parent)


class HubManger:

    _instance = None
    db_conn_status = 'disconnected'
    db = None
    db_name = 'morpheus2'
    db_host = ''
    db_port = 5432
    db_user = 'morpheus'
    db_password = 'Buster77!'
    uuid = str(uuid.uuid4())
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.connect_db_hub(cls._instance)
                
        return cls._instance

    def __init__(cls):
        pass

    def connect_db_hub(cls, signal_grp=None):
        thread = threading.Thread(target=cls.connect_db_hub_thread, daemon=True)
        thread.start()

    def connect_db_hub_thread(cls):
        msg_dict = {}
        msg_dict['area'] = 'system'
        signal = Signal()
        try:
            db_serv_dict = cls.get_current_db_hub()
            cls.db_host = db_serv_dict['ip_addr']
            cls.db = PostgresqlDatabase(cls.db_name, host=cls.db_host, port=cls.db_port, user=cls.db_user,
                password=cls.db_password)
            #run a test query to see if connection is successful
            from system.models import Room
            test_qs = Room.select()
            count = test_qs.count()
        except Exception as e:
            traceback.print_exc()
            cls.db_conn_status = 'error'
            msg_dict['type'] = 'message'
            msg_dict['status'] = 'error'
            msg_dict['message'] = 'Error connecting to database hub.'
            signal.send(cls.uuid, msg_dict, True)
            msg_dict['type'] = 'update'
            msg_dict['item'] = 'hub_db_connect'
            msg_dict['value'] = cls.db_conn_status
            signal.send(cls.uuid, msg_dict, True)
            logger.log('connect_db_hub', msg_dict['message'], str(e) + traceback.format_exc(), 'ERROR') 
            return msg_dict
        else:
            cls.db_conn_status = 'connected'
            msg_dict['type'] = 'message'
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Connected to database hub.'
            signal.send(cls.uuid, msg_dict, True)
            msg_dict['type'] = 'update'
            msg_dict['item'] = 'hub_db_connect'
            msg_dict['value'] = cls.db_conn_status
            signal.send(cls.uuid, msg_dict, True)
            logger.log('connect_db_hub', 'Connected to database hub.', 'Database hub: ' + cls.db_host, 'INFO')

    def get_db_status(cls):
        signal = Signal()
        msg_dict = {}
        msg_dict['area'] = 'system'
        msg_dict['type'] = 'update'
        msg_dict['item'] = 'hub_db_connect'
        msg_dict['value'] = cls.db_conn_status
        signal.send(cls.uuid, msg_dict, True)   

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
            
    def get_client_ip_addr(cls):
        f = open(BASE_DIR + '/settings.json', 'r')
        settings = json.load(f)
        client_ip = settings['client_ip_addr']
        return client_ip
            
    def set_current_hub(cls, hub_id):
        msg_dict = {}
        msg_dict['area'] = 'system'
        msg_dict['type'] = 'message'
        try: 
            f = open(BASE_DIR + '/settings.json', 'r')
            settings = json.load(f)
            settings['current_hub_id'] = hub_id
            f = open(BASE_DIR + '/settings.json', 'w')
            f.write(json.dumps(settings, indent=4))
            f.close()
        except Exception as e:
            msg_dict['status'] = 'error'
            msg_dict['message'] = 'Error setting Hub.'
            logger.log('set_current_hub', msg_dict['message'], str(e) + traceback.format_exc(), 'ERROR') 
            return msg_dict
        else:
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Hub set.  Please restart Morpheus.'
            logger.log('set_current_hub', 'Hub set.  Please restart Morpheus.', 'Database hub: ' + str(hub_id), 'INFO')
            return msg_dict
            
    def get_current_db_hub(cls):
        msg_dict = {}
        msg_dict['area'] = 'system'
        msg_dict['type'] = 'message'
        try: 
            f = open(BASE_DIR + '/settings.json', 'r')
            settings = json.load(f)
            current_db_hub = settings['current_db_hub_id']
            hub_list = settings['hub_list']
            for hub in hub_list:
                if hub['id'] == current_db_hub:
                    return hub
        except Exception as e:
            msg_dict['status'] = 'error'
            msg_dict['message'] = 'Error setting Hub.'
            logger.log('set_current_hub', msg_dict['message'], str(e) + traceback.format_exc(), 'ERROR') 
            return msg_dict
        else:
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Hub set.  Please restart Morpheus.'
            logger.log('set_current_hub', 'Hub set.  Please restart Morpheus.', 'Database hub: ' + str(hub_id), 'INFO')
            return msg_dict
            
    def set_current_db_hub(cls, hub_id):
        msg_dict = {}
        msg_dict['area'] = 'system'
        msg_dict['type'] = 'message'
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
        msg_dict['area'] = 'system'
        msg_dict['type'] = 'message'
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
        msg_dict['area'] = 'system'
        msg_dict['type'] = 'message'
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
        msg_dict['area'] = 'system'
        msg_dict['type'] = 'message'
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
    hub_connected = 'disconnected'
    hub_host = ''
    hub_port = 8999
    hub_mgr = HubManger()
    websocket = None
    client = None
    uuid = str(uuid.uuid4())
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.hub_host = cls.hub_mgr.get_current_hub()['ip_addr']
           
        return cls._instance
    
    def __init__(cls):
        pass

    def connect_socket(cls):
        msg_dict = {}
        signal = Signal()
        msg_dict['area'] = 'system'
        msg_dict['type'] = 'message'
        msg_dict['status'] = 'info'
        msg_dict['message'] = 'Connecting to hub...' 
        signal.send(cls.uuid, msg_dict, True)
        try:
            cls.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cls.client.settimeout(5.0)
            #cls.client.bind(('', cls.hub_port))
            cls.client.connect((cls.hub_host, cls.hub_port))
        except Exception as e:
            traceback.print_exc()
            cls.hub_connected = 'error'
            msg_dict['area'] = 'system'
            msg_dict['type'] = 'message'
            msg_dict['status'] = 'error'
            msg_dict['message'] = 'Error connecting to hub.'
            
            logger.log('connect_socket', msg_dict['message'], str(e) + traceback.format_exc(), 'ERROR') 
            signal.send(cls.uuid, msg_dict, True)
            return msg_dict
        else:
            cls.hub_connected = 'connected'
            msg_dict['area'] = 'system'
            msg_dict['type'] = 'message'
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Connected to hub.'
            signal.send(cls.uuid, msg_dict, True)
            logger.log('connect_socket', 'Connected to hub.', 'Hub: ' + cls.hub_host, 'INFO')
            cls.update_status()
            return msg_dict
        
    def disconnect_socket(cls):
        print('Disconnecting from hub...', cls.hub_connected)
        msg_dict = {}
        send_msg_dict = {}
        send_msg_dict['area'] = 'system'
        send_msg_dict['type'] = 'command'
        send_msg_dict['value'] = 'socket_disconnect'
        msg_dict['area'] = 'system'
        msg_dict['type'] = 'message'
        msg_dict['status'] = 'info'
        msg_dict['message'] = 'Disconnecting from hub...' 
        signal = Signal()
        signal.send(cls.uuid, msg_dict, True)
        try:
            if cls.hub_connected == 'connected':
                message = json.dumps(send_msg_dict)
                msg = message.encode('utf-8')
                cls.client.send(msg)
                result = cls.client.recv(4096).decode('utf-8')
                print('Disconnect result:', result)
            
        except Exception as e:
            traceback.print_exc()
            cls.hub_connected = 'error'
            msg_dict['status'] = 'error'
            msg_dict['message'] = 'Error sending disconnect message to hub.'
            logger.log('disconnect_socket', msg_dict['message'], str(e) + traceback.format_exc(), 'ERROR') 
            signal.send(cls.uuid, msg_dict, True)
            return msg_dict
        else:
            cls.hub_connected = 'disconnected'
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Succesfully disconnected from hub.'
            signal.send(cls.uuid, msg_dict, True)
            logger.log('disconnect_socket', 'Disconnected from hub.', 'Hub: ' + cls.hub_host, 'INFO')
            return msg_dict

    def send(cls, msg_dict):
        try:
            if cls.hub_connected == 'connected' or cls.hub_connected == 'warning':
                message = json.dumps(msg_dict)
                msg = message.encode('utf-8')
                cls.client.send(msg)
        except Exception as e:
            traceback.print_exc()
            logger.log('send', 'Error sending to hub.', str(e) + traceback.format_exc(), 'ERROR')
        
    def update_status(cls):
        signal = Signal()
        msg_dict = {}
        msg_dict['area'] = 'system'
        msg_dict['type'] = 'update'
        msg_dict['item'] = 'hub_connect'
        msg_dict['value'] = cls.hub_connected
        signal.send(cls.uuid, msg_dict, True)

    def keep_alive(cls):
        msg_dict = {}
        strikes = 0
        
        while True:
            try:
                #print('Keep alive thread running...' + cls.hub_connected)
                if cls.hub_connected == 'connected' or cls.hub_connected == 'warning':
                    msg_dict['area'] = 'system'
                    msg_dict['type'] = 'command'
                    msg_dict['value'] = 'socket_keepalive'
                    message = json.dumps(msg_dict)
                    msg = message.encode('utf-8')
                    cls.client.send(msg)
                    result = cls.client.recv(4096).decode('utf-8')
                    #print('keep alive result:', result)
                    strikes = 0
                else:
                    print('Keep alive thread stopped Hub not connected...')
                    break    
            
            except socket.timeout:
                strikes += 1
                msg_dict['area'] = 'system'
                msg_dict['type'] = 'message'
                msg_dict['status'] = 'warning'
                msg_dict['message'] = 'Keep alive socket timeout, failed attemps: ' + str(strikes) 
                logger.log('keep_alive', msg_dict['message'], '', 'WARNING') 
                cls.hub_connected = 'warning' 
                signal.send(cls.uuid, msg_dict, True)
                if strikes > 5:
                    result_dict = cls.reconnect_socket()
                    print('Reconnect result:', result_dict)
                    if result_dict['status'] == 'error':
                        break
                    elif result_dict['status'] == 'success':
                        strikes = 0

            except Exception as e:
                print('Error sending keep alive to hub:')
                strikes += 1    
                logger.log('keep_alive', 'Error sending keep alive to hub. Strikes: ' + str(strikes), str(e) + traceback.format_exc(), 'WARNING')
                msg_dict['area'] = 'system'
                msg_dict['type'] = 'message'
                msg_dict['status'] = 'warning'
                msg_dict['message'] = 'Error sending keep alive to hub, failed attemps: ' + str(strikes)  
                cls.hub_connected = 'warning' 
                signal = Signal()
                signal.send(cls.uuid, msg_dict, True)
                if strikes > 5:
                    result_dict = cls.reconnect_socket()
                    if result_dict['status'] == 'error':
                        break
                    elif result_dict['status'] == 'success':
                        strikes = 0
            
                    
            finally:
                cls.update_status()
                time.sleep(5) 
    
    def start_hub_connection(cls):
        result_dict = cls.connect_socket()
        if result_dict['status'] == 'success':
            print('Connected to hub. Starting keep alive thread...')
            thread = threading.Thread(target=cls.keep_alive, daemon=True)
            thread.start()

    ####TODO - add reconnect to hub if connection is lost
    def reconnect_socket(cls):
        msg_dict = {
            'area': 'system',
        }
        signal = Signal()
        try:
            #reconnect try
            a = 1 / 0 #always throws an error to test reconnect
        except Exception as e:
            cls.hub_connected = 'error'
            msg_dict['type'] = 'message'
            msg_dict['status'] = 'error'
            msg_dict['message'] = 'Error reconnecting to hub, connection terminated.'
            signal.send(cls.uuid, msg_dict, True)
            logger.log('reconnect_socket', msg_dict['message'], str(e) + traceback.format_exc(), 'ERROR')
            return msg_dict
            
        else:
            cls.hub_connected = 'connected'
            msg_dict['type'] = 'message'
            msg_dict['message'] = 'Reconnected to hub.'
            logger.log('reconnect_socket', msg_dict['message'], '', 'INFO')
            msg_dict['type'] = 'update'
            msg_dict['item'] = 'hub_connect'
            msg_dict['value'] = 'connected'
            return msg_dict
        