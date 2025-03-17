
import traceback
from system.logging import SystemLogger  
from hue.models import HueBridge, HueDevice, HueLight, HueButton
from system.models import DeviceType

logger = SystemLogger(__name__)

class HueBridgeUtils():
    def __init__(self):
        pass


    def set_url(self, bridge_id):
        bridge = HueBridge.get(HueBridge.id == bridge_id)
        self.username = bridge.username
        self.ip_addr = bridge.ip_addr
        self.key = bridge.key
        self.name = bridge.name

        self.url_pre = 'http://' + self.ip_addr
        self.headers = {"hue-application-key": self.username}


    def sync_bridge(self, bridge_id, message_function=None):
        msg_dict = {}

    def sync_device_types(self, bridge_id, message_function=None):
        hue_dev = HueDeviceTypes()
        msg_dict = {}
        if message_function:
            msg_dict['status'] = 'info'
            msg_dict['message'] = 'Syncing device types'
            message_function(msg_dict)
        try:
            device_list = hue_dev.get_device_list()
            for device in device_list:
                if device['system_sync']:
                    dev_type = DeviceType.get_or_none(DeviceType.name == device['device_type'])
                    if not dev_type:
                        dev_type = DeviceType.create(name=device['device_type'], display_name=device['display_name'], interface='hue', capability=device['capability'])
                        msg_dict['status'] = 'info'
                        msg_dict['message'] = 'Device type created: ' + device['display_name']
                        if message_function:
                            message_function(msg_dict)
                    else:
                        msg_dict['status'] = 'info'
                        msg_dict['message'] = 'Device type exists: ' + device['display_name']
                        if message_function:
                            message_function(msg_dict)

        

        except Exception as e:
            logger.log('sync_device_types', 'Error syncing device types.', str(e) + traceback.format_exc(), 'ERROR')
            msg_dict['status'] = 'error'
            msg_dict['message'] = 'Error syncing device types. ' + str(e)
            if message_function:
                message_function(msg_dict)
            return msg_dict
        
        else:
            logger.log('sync_device_types', 'Device types synced.', 'Device types synced successfully.', 'INFO')
            msg_dict['status'] = 'success'
            msg_dict['message'] = 'Device types synced successfully.'
            if message_function:
                message_function(msg_dict)
            return msg_dict
            
    # def sync_device_db(self, hub_id, message_function=None):
    #     try:
    #             msg_dict = {}
    #             if message_function:
    #                 msg_dict['status'] = 'info'
    #                 msg_dict['message'] = 'Syncing Hue Devices'
    #                 message_function(msg_dict)
    #             self.hub_id = hub_id
    #             self.set_url(self.hub_id)
    #             devices = hub.get_items('devices')
    #             for device in devices:
    #                 device_qs = HueDevice.objects.filter(hue_id=device['id'])
    #                 if device_qs:
    #                     device_qs[0].name = device['metadata']['name']
    #                     device_qs[0].software_version = device['product_data']['software_version']
    #                     device_qs[0].save()
    #                 else:
    #                     #create parent device
    #                     new_device = HueDevice(
    #                         product_name = device['product_data']['product_name'],
    #                         hub_id = hub_id,
    #                         hue_id = device['id'],
    #                         model_id = device['product_data']['model_id'],
    #                         manufacturer_name = device['product_data']['manufacturer_name'],
    #                         software_version = device['product_data']['software_version'],
    #                         name = device['metadata']['name'],
    #                     )
    #                     services = device['services']
    #                     #Get the zigbee service rid
    #                     for service in services:
    #                         service_dict = dict(service)
    #                         if service_dict['rtype'] == 'zigbee_connectivity':
    #                             new_device.zigbee_rid = service_dict['rid']

    #                     #get the device type, add it
                        
    #                     hue_type = self.huetype_from_modelid(device['product_data']['model_id'])
    #                     new_device.hue_device_type = hue_type
                        
    #                     if hue_type == 'COLORLAMP' or hue_type == 'WHITELAMP':
    #                         new_light = HueLight()
    #                         new_device.save()
    #                         new_light.device = new_device
    #                         for service in services:
    #                             service_dict = dict(service)
    #                             if service_dict['rtype'] == 'light':
    #                                 new_light.rid = service_dict['rid']
    #                                 if hue_type == 'COLORLAMP':
    #                                     #get light details from Hub to get Gamut
    #                                     light_item = hub.get_item('light',service_dict['rid'])
    #                                     new_light.gamut_type = light_item['color']['gamut_type']
    #                         new_light.save()
                        
    #                     if hue_type == 'DIMSWITCH':
    #                         #A switch will have multiple buttons and a power state rid
    #                         new_device.save()
    #                         button_num = 1
    #                         for service in services:
    #                             service_dict = dict(service)
    #                             if service_dict['rtype'] == 'device_power':
    #                                 new_device.power_rid = service_dict['rid']
    #                                 new_device.save()
    #                             if service_dict['rtype'] == 'button':
    #                                 new_button = HueButton()
    #                                 new_button.device = new_device
    #                                 new_button.rid = service_dict['rid']
    #                                 new_button.name = 'Button ' + str(button_num)
    #                                 button_num += 1
    #                                 new_button.save()

    #                     if hue_type == 'HUB':
    #                         new_device.save()
    #                         for service in services:
    #                             service_dict = dict(service)
    #                             if service_dict['rtype'] == 'bridge':
    #                                 new_device.bridge_rid = service_dict['rid']
    #                                 new_device.save()

                            
    #                     else:
    #                         self.send_message('update_msg', 'Item type not found, not added to DB' + device['product_data']['model_id'])
    #                         logger.log('sync_device_db','Sync Databse: Item type not found, not added to DB', 'Hue Type: ' + device['product_data']['model_id'], 'ERROR')
    #             #remove devices that are no longer in the hub
    #             self.send_message('update_msg', 'Checking for devices not in hub to remove')
    #             morph_devices = HueDevice.objects.all(morph_sync=True)
    #             for morph_device in morph_devices:
    #                 exists = False
    #                 for device in devices:
    #                     if morph_device.hue_id == device['id']:
    #                         exists = True
    #                         break
    #                 if not exists:
    #                     morph_device.delete()
    #                     self.send_message('update_msg', 'Device Removed: ' + morph_device.name)
                

    #             logger.log('sync_device_db','Sync Databse: Completed', 'Completed succesfully', 'INFO')
    #             self.send_message('update_msg', 'Device Sync Complete')
    #         except Exception as error:
    #             logger.log('sync_device_db','Sync Databse: Item type not found, not added to DB', 'Hue Type: ' + device['product_data']['model_id'], 'ERROR')
    #             self.send_message('update_msg', 'Device Sync Failed') 
  

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
                'system_sync': False

            },
            {
                'display_name': 'Hub',
                'device_type': 'HUB',
                'system_sync': False

            },
            
        ]
    
    def get_device_list(self):
        return self.device_list