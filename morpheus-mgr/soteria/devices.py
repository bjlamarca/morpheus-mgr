import traceback
from system.logger import SystemLogger
from devices.models import DeviceType
from system.signals import Signal

logger = SystemLogger(__name__)

class SoteriaDeviceTypes():
    #
    def __init__(self):
        self.device_list = [
            {
                'display_name': 'Morpheus Manager (Soteria)',
                'device_type': 'SOTERIAMANAGER',
                'capability': 'Controller',
                'system_sync': True

            },
        ]
        
    def get_device_list(self):
        return self.device_list
    
    def get_devtype_obj(self, model_id):
        for model in self.hue_model_type:
            if model_id == model[0]:
                return DeviceType.get_or_none(DeviceType.name == model[1])
        return None
    
class SoteriaUtilities():
    def sync_device_types(self):
            soteria_dev_types = SoteriaDeviceTypes()
            msg_dict = {'sender': {
                'type': 'local',
                'uuid': self.uuid,}}
            signal = Signal()
            msg_dict['area'] = 'soteria'
            msg_dict['type'] = 'message'
            msg_dict['status'] = 'clear'
            signal.send(msg_dict, True)
            msg_dict['status'] = 'info'
            msg_dict['message'] = 'Syncing device types'
            signal.send(msg_dict, True)
            try:
                device_list = soteria_dev_types.get_device_list()
                for device in device_list:
                    dev_type = DeviceType.get_or_none(DeviceType.name == device['device_type'])
                    if not dev_type:
                        dev_type = DeviceType.create(name=device['device_type'], display_name=device['display_name'], interface='soteria', capability=device['capability'])
                        msg_dict['status'] = 'info'
                        msg_dict['message'] = 'Device type created: ' + device['display_name']
                        signal.send(msg_dict, True)
                    else:
                        msg_dict['status'] = 'info'
                        msg_dict['message'] = 'Device type exists: ' + device['display_name']
                        signal.send(msg_dict, True)

            

            except Exception as e:
                traceback.print_exc()
                logger.log('sync_device_types', 'Error syncing device types.', str(e) + traceback.format_exc(), 'ERROR')
                msg_dict['status'] = 'error'
                msg_dict['message'] = 'Error syncing device types. ' + str(e)
                signal.send(msg_dict, True)
                return msg_dict
            
            else:
                logger.log('sync_device_types', 'Device types synced.', 'Device types synced successfully.', 'INFO')
                msg_dict['status'] = 'success'
                msg_dict['message'] = 'Device types synced successfully.'
                signal.send(msg_dict, True)
                return msg_dict
