
from system.logging import SystemLogger  
from hue.models import HueBridge
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
                    dev_type = DeviceType.get_or_none(DeviceType.device_type == device['device_type'])
                    if not dev_type:
                        dev_type = DeviceType.create(device_type=device['device_type'], display_name=device['display_name'], capability=device['capability'])
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
            logger.log('sync_device_types', 'Error syncing device types.', 'Error: ' + str(e), 'ERROR')
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
                'morph_sync': True

            },
            {
                'display_name': 'Hue Dimmer Switch',
                'hue_device_type': 'HUEDIMSWITCH',
                'morph_name': 'HUEDIMSWITCH',
                'morph_display_name': 'Hue Dimmer Switch',
                'morph_sync': False

            },
            {
                'display_name': 'Hub',
                'hue_device_type': 'HUB',
                'morph_name': 'HUEHUB',
                'morph_display_name': 'Hue Hub',
                'morph_sync': False

            },
            
        ]
    
    def get_device_list(self):
        return self.device_list