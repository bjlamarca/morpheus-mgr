import traceback, ipaddress
from system.logger import SystemLogger
from devices.models import DeviceType
from system.signals import Signal
from soteria.models import SoteriaDevice

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
    def __init__(self):
        self.device_list = []
        
    
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
    
    def get_device_list(self):
        device_qs = SoteriaDevice.select()
        for device in device_qs:
            self.device_list.append({
                'device_id': device.id,
                'device_type': device.device_type.name,
                'device_name': device.name,
                'identifier': device.identifier,
                'device_type_id': device.device_type.id,
                'ip_address': device.ip_address,
                'mac_address': device.mac_address,
                'last_seen': device.last_seen,
                'supervised': device.supervised,
                'connected': device.connected,
                'model_number': device.model_number
            })
        return self.device_list
    
    def delete_device(self, device_id):
        responce = {'type': 'message'}
        try:
            device = SoteriaDevice.get(SoteriaDevice.id == device_id)
            device.delete_instance()
            responce['status'] = 'success'
            responce['message'] = 'Device deleted successfully'
            logger.log('delete_device', 'Bridge deleted', 'Bridge deleted successfully: ' + str(device), 'INFO')
            return responce
        except Exception as e:
            logger.log('delete_device', 'Error deleting device', 'Error: ' + str(e) + traceback.format_exc(), 'ERROR')
            responce['status'] = 'error'
            responce['message'] = 'Error deleting device: ' + str(e)
            return responce

    def edit_device(self, device_dict):
        responce = {'type': 'message'}
        if not device_dict['name'] or not device_dict['ip_address'] or not device_dict['device_type']:
            responce['status'] = 'error'
            responce['message'] = 'Check required fields'
            return responce
        try:
            ipaddress.ip_address(device_dict['ip_address'])
        except ValueError:
            responce['status'] = 'error'
            responce['message'] = 'Invalid IP Address'
            return responce 
        try:
            device = SoteriaDevice.get_or_none(SoteriaDevice.id == device_dict['device_id'])
            if not device:
                responce['status'] = 'error'
                responce['message'] = 'Device not found'
                return responce
            device.device_type = device_dict['device_type']
            device.name = device_dict['name']
            device.identifier = device_dict['identifier']
            device.ip_address = device_dict['ip_address']
            device.mac_address = device_dict['mac_address']
            device.supervised = device_dict['supervised']
            device.model_number = device_dict['model_number']
            device.save()
            responce['status'] = 'success'
            responce['device'] = device
            logger.log('edit_device', 'Bridge edited', 'Bridge edited successfully: ' + str(device), 'INFO')
            return responce
        except Exception as e:
            logger.log('edit_device', 'Error editing device', 'Error: ' + str(e) + traceback.format_exc(), 'ERROR')
            responce['status'] = 'error'
            responce['message'] = 'Error editing device ' + str(e)
            return responce 

    def add_device(self, device_dict):
        responce = {'type': 'message'}
        if not device_dict['name'] or not device_dict['ip_address'] or not device_dict['device_type']:
            responce['status'] = 'error'
            responce['message'] = 'required'
            return responce
        try:
            ipaddress.ip_address(device_dict['ip_address'])
        except ValueError:
            responce['status'] = 'error'
            responce['message'] = 'Invalid IP Address'
            return responce
        
        try:
            device = SoteriaDevice.create(
                device_type=device_dict['device_type'],
                identifier=device_dict['identifier'],
                name=device_dict['name'],
                ip_address=device_dict['ip_address'],
                mac_address=device_dict['mac_address'],
                supervised=device_dict['supervised'],
                model_number=device_dict['model_number']
            )
            responce['status'] = 'success'
            responce['device'] = device            
            logger.log('add_device', 'Bridge added', 'Bridge added successfully: ' + str(device), 'INFO')
            return responce
        
        except Exception as e:
            logger.log('add_device', 'Error adding device', 'Error: ' + str(e) + traceback.format_exc(), 'ERROR')
            responce['status'] = 'error'
            responce['message'] = 'Error adding device ' + str(e)
            return responce