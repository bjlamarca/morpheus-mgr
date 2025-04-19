import json, requests, traceback, time, threading
from system.logger import SystemLogger  
from hue.models import HueBridge, HueDevice, HueLight, HueButton
from system.models import DeviceType
from system.signals import Signal

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = SystemLogger(__name__)

class HueBridgeUtils():
    def __init__(self):
        pass

    def set_bridge(self, bridge_id):
        bridge = HueBridge.get(HueBridge.id == bridge_id)
        self.username = bridge.username
        self.ip_addr = bridge.ip_addr
        self.key = bridge.key
        self.name = bridge.name

        self.url_pre = 'https://' + self.ip_addr
        self.header = {"hue-application-key": self.username}

    def sync_device_types(self, signal_grp=None):
        hue_dev_types = HueDeviceTypes()
        msg_dict = {}
        signal = Signal()
        msg_dict['area'] = 'system'
        msg_dict['type'] = 'message'
        msg_dict['status'] = 'clear'
        signal.send(signal_grp, 'sync_device_types', msg_dict, True)
        msg_dict['status'] = 'info'
        msg_dict['message'] = 'Syncing device types'
        if signal_grp:
            signal.send(signal_grp, 'sync_device_types', msg_dict, True)
        try:
            device_list = hue_dev_types.get_device_list()
            for device in device_list:
                dev_type = DeviceType.get_or_none(DeviceType.name == device['device_type'])
                if not dev_type:
                    dev_type = DeviceType.create(name=device['device_type'], display_name=device['display_name'], interface='hue', capability=device['capability'])
                    msg_dict['status'] = 'info'
                    msg_dict['message'] = 'Device type created: ' + device['display_name']
                    if signal_grp:
                        signal.send(signal_grp, 'sync_device_types', msg_dict, True)
                else:
                    msg_dict['status'] = 'info'
                    msg_dict['message'] = 'Device type exists: ' + device['display_name']
                    if signal_grp:
                        signal.send(signal_grp, 'sync_device_types', msg_dict, True)

        

        except Exception as e:
            traceback.print_exc()
            logger.log('sync_device_types', 'Error syncing device types.', str(e) + traceback.format_exc(), 'ERROR')
            msg_dict['status'] = 'error'
            msg_dict['message'] = 'Error syncing device types. ' + str(e)
            if signal_grp:
                signal.send(signal_grp, 'sync_device_types', msg_dict, True)
            return msg_dict
        
        else:
            logger.log('sync_device_types', 'Device types synced.', 'Device types synced successfully.', 'INFO')
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Device types synced successfully.'
            if signal_grp:
                signal.send(signal_grp, 'sync_device_types', msg_dict, True)
            return msg_dict

    def sync_bridge(self, bridge_id, signal_grp=None):
        thread = threading.Thread(target=self.sync_bridge_thread, args=(bridge_id, signal_grp))
        thread.daemon = True
        thread.start()

    def sync_bridge_thread(self, bridge_id, signal_grp=None):
        try:
                hue_dev_types = HueDeviceTypes()
                msg_dict = {}
                signal = Signal()
                msg_dict['area'] = 'system'
                msg_dict['type'] = 'message' 
                msg_dict['status'] = 'clear'
                msg_dict['status'] = 'info'
                msg_dict['message'] = 'Syncing Hue Devices'
                if signal_grp:
                    signal.send(signal_grp, 'sync_bridge', msg_dict, True)
                self.bridge_id = bridge_id
                self.set_bridge(self.bridge_id)
                bridge_devices = self.get_items('devices')
                for device in bridge_devices:
                    time.sleep(.05)
                    device_obj = HueDevice.get_or_none(HueDevice.hue_id == device['id'])
                    if device_obj:
                        device_obj.name = device['metadata']['name']
                        device_obj.software_version = device['product_data']['software_version']
                        device_obj.save()
                        msg_dict['status'] = 'info'
                        msg_dict['message'] = 'Device Updated: ' + device_obj.name
                        if signal_grp:
                            signal.send(signal_grp, 'sync_bridge', msg_dict, True)
                    else:
                        #create parent device
                        new_device = HueDevice(
                            product_name = device['product_data']['product_name'],
                            bridge_id = self.bridge_id,
                            hue_id = device['id'],
                            model_id = device['product_data']['model_id'],
                            manufacturer_name = device['product_data']['manufacturer_name'],
                            software_version = device['product_data']['software_version'],
                            name = device['metadata']['name'],
                            morph_sync = False,
                        )
                        services = device['services']
                        #Get the zigbee service rid
                        for service in services:
                            service_dict = dict(service)
                            if service_dict['rtype'] == 'zigbee_connectivity':
                                new_device.zigbee_rid = service_dict['rid']

                        #get the device type, add it
                        
                        hue_model_id = (device['product_data']['model_id'])
                        device_type = hue_dev_types.get_devtype_obj(hue_model_id)
                        new_device.device_type = device_type
                        
                        if device_type.name == 'HUECOLORLAMP' or device_type.name == 'HUEWHITELAMP':
                            new_light = HueLight()
                            new_device.save()
                            new_light.device = new_device
                            for service in services:
                                service_dict = dict(service)
                                if service_dict['rtype'] == 'light':
                                    new_light.rid = service_dict['rid']
                                    if device_type.name == 'HUECOLORLAMP':
                                        #get light details from Hub to get Gamut
                                        light_item = self.get_item('light',service_dict['rid'])
                                        new_light.gamut_type = light_item['color']['gamut_type']
                            new_light.save()
                        
                        if device_type.name == 'HUEDIMSWITCH':
                            #A switch will have multiple buttons and a power state rid
                            new_device.save()
                            button_num = 1
                            for service in services:
                                service_dict = dict(service)
                                if service_dict['rtype'] == 'device_power':
                                    new_device.power_rid = service_dict['rid']
                                    new_device.save()
                                if service_dict['rtype'] == 'button':
                                    new_button = HueButton()
                                    new_button.device = new_device
                                    new_button.rid = service_dict['rid']
                                    new_button.name = 'Button ' + str(button_num)
                                    button_num += 1
                                    new_button.save()

                        if device_type.name == 'HUEBRIDGE':
                            new_device.save()
                            for service in services:
                                service_dict = dict(service)
                                if service_dict['rtype'] == 'bridge':
                                    new_device.bridge_rid = service_dict['rid']
                                    new_device.save()

                        msg_dict['status'] = 'info'
                        msg_dict['message'] = 'Device Added: ' + new_device.name
                        if signal_grp:
                            signal.send(signal_grp, 'sync_bridge', msg_dict, True)
                        else:
                            msg_dict['status'] = 'error'
                            msg_dict['message'] = 'Item type not found, not added to DB' + device['product_data']['model_id']
                            if signal_grp:
                                signal.send(signal_grp, 'sync_bridge', msg_dict, True)
                            logger.log('sync_device_db','Sync Databse: Item type not found, not added to DB', 'Hue Type: ' + device['product_data']['model_id'], 'ERROR')
                
                #remove devices that are no longer in the hub
                msg_dict['status'] = 'info'
                msg_dict['message'] = 'Checking for devices not in hub to remove'
                if signal_grp:
                    signal.send(signal_grp, 'sync_bridge', msg_dict, True)
                devices = HueDevice.select().where(HueDevice.morph_sync==True)
                for device in devices:
                    exists = False
                    for device in devices:
                        if device.hue_id == device['id']:
                            exists = True
                            break
                    if not exists:
                        device.delete()
                        if signal_grp:
                            msg_dict['status'] = 'info'
                            msg_dict['message'] = 'Device Removed: ' + device.name
                            signal.send(signal_grp, 'sync_bridge', msg_dict, True)
                

                logger.log('sync_device_db','Sync Databse: Completed', 'Completed succesfully', 'INFO')
                msg_dict['status'] = 'success'
                msg_dict['message'] = 'Syncing Hue Devices completed successfully'
                if signal_grp:
                    signal.send(signal_grp, 'sync_bridge', msg_dict, True)
        
        except Exception as error:
            traceback.print_exc()
            logger.log('sync_device_db','Syncing Hue Databse failed', str(error), 'ERROR')
            msg_dict['status'] = 'error'
            msg_dict['message'] = 'Syncing Hue Devices failed. ' + str(error)
            if signal_grp:
                    signal.send(signal_grp, 'sync_bridge', msg_dict, True)
            
    def get_items(self, item):
        if item == 'lights':
            url = self.url_pre + '/clip/v2/resource/light'
        elif item == 'devices':
            url = self.url_pre + '/clip/v2/resource/device'
        elif item == 'buttons':
            url = self.url_pre + '/clip/v2/resource/button'
        elif item == 'zigbee':
            url = self.url_pre + '/clip/v2/resource/zigbee_connectivity'
        elif item == 'power':
            url = self.url_pre + '/clip/v2/resource/device_power'
        else:
            logger.log('get_items', 'Not vaild Item(s)', url,  'ERROR')
            return None
        try:
            result = requests.get(url, headers=self.header, verify=False)
            return_dict = dict(json.loads(result.text))
            errors_list = return_dict['errors']
            if bool(errors_list):
                logger.log('get_items','Hub returned Errors attempting to get Items', errors_list, 'ERROR')
                return None
            else:
                data_list = return_dict['data']
                return data_list
        except Exception as error:
            traceback.print_exc()
            logger.log('get_items','Cannot retrieve items from Hub.', str(error), 'ERROR')
            return None

    #Get an item from the hub, returns a dict
    def get_item(self, item, device_id=None):
        if item == 'device':
            url = self.url_pre + '/clip/v2/resource/device/' + device_id
        elif item == 'light':
            url = self.url_pre + '/clip/v2/resource/light/' + device_id
        elif item == 'button':
            url = self.url_pre + '/clip/v2/resource/button/' + device_id
        elif item == 'zigbee':
            url = self.url_pre + '/clip/v2/resource/zigbee_connectivity/' + device_id
        elif item == 'power':
            url = self.url_pre + '/clip/v2/resource/device_power/' + device_id
        else:
            logger.log('get_item', 'Get All Devices','Not a vaild Item(s)', 'ERROR')
        try:
            result = requests.get(url, headers=self.header, verify=False)
            return_dict = dict(json.loads(result.text))
            errors_list = return_dict['errors']
            if bool(errors_list):
                logger.log('get_item','Cannot retrieve data from Hub', errors_list, 'ERROR')
                return None
            else:
                data_list = return_dict['data']
                #return first (only) item from list as a dict
                return dict(data_list[0])
        except Exception as error:
            traceback.print_exc()
            logger.log('get_item','Cannot retrieve item from Hub.', error, 'ERROR')

class HueDeviceTypes():
    #
    def __init__(self):
        self.device_list = [
            {
                'display_name': 'Hue White Light',
                'device_type': 'HUEWHITELAMP',
                'capability': 'switch, dimmer',
                'system_sync': True

            },
            {
                'display_name': 'Hue Color Light',
                'device_type': 'HUECOLORLAMP',
                'capability': 'color, switch, dimmer',
                'system_sync': True

            },
            {
                'display_name': 'Hue Dimmer Switch',
                'device_type': 'HUEDIMSWITCH',
                'capability': 'switch, dimmer',
                'system_sync': False

            },
            {
                'display_name': 'Hue Bridge',
                'device_type': 'HUEBRIDGE',
                'capability': 'bridge',
                'system_sync': False

            },
            
        ]
        self.hue_model_type = [
            ['LCA009','HUECOLORLAMP'],
            ['LCT014','HUECOLORLAMP'],
            ['LCA003','HUECOLORLAMP'],
            ['LWB014','HUEWHITELAMP'],
            ['LCA002','HUECOLORLAMP'],
            ['BSB002','HUEBRIDGE'],
            ['LCA005','HUECOLORLAMP'],
            ['LCT016','HUECOLORLAMP'],
            ['RWL020','HUEDIMSWITCH'],
            ['LCA009', 'HUECOLORLAMP'],
        ]
    
    def get_device_list(self):
        return self.device_list
    
    def get_devtype_obj(self, model_id):
        for model in self.hue_model_type:
            if model_id == model[0]:
                return DeviceType.get_or_none(DeviceType.name == model[1])
        return None
    


    
    
