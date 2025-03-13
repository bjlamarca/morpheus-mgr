import ipaddress
from hue.models import HueBridge
from system.logging import SystemLogger
logger = SystemLogger(__name__)



class HueUtilities():

    def add_bridge(self, name, ip_addr, username, key):
        responce = {}
        if not name or not ip_addr or not username or not key:
            responce['status'] = 'error'
            responce['message'] = 'All fields are required'
            return responce
        try:
            ipaddress.ip_address(ip_addr)
        except ValueError:
            responce['status'] = 'error'
            responce['message'] = 'Invalid IP Address'
            return responce
        
        try:
            bridge = HueBridge.create(name=name, ip_addr=ip_addr, username=username, key=key)
            responce['status'] = 'success'
            responce['bridge'] = bridge            
            logger.log('add_bridge', 'Bridge added', 'Bridge added successfully: ' + str(bridge), 'INFO')
            return responce
        
        except Exception as e:
            logger.log('add_bridge', 'Error adding bridge', 'Error: ' + str(e), 'ERROR')
            responce['status'] = 'error'
            responce['message'] = 'Error adding bridge ' + str(e)
            return responce
        
    def edit_bridge(self, bridge_id, name, ip_addr, username, key):
        responce = {}
        if not name or not ip_addr or not username or not key:
            responce['status'] = 'error'
            responce['message'] = 'All fields are required'
            return responce
        try:
            ipaddress.ip_address(ip_addr)
        except ValueError:
            responce['status'] = 'error'
            responce['message'] = 'Invalid IP Address'
            return responce
        try:
            bridge = HueBridge.get_by_id(bridge_id)
            bridge.name = name
            bridge.ip_addr = ip_addr
            bridge.username = username
            bridge.key = key
            bridge.save()
            responce['status'] = 'success'
            responce['bridge'] = bridge
            logger.log('edit_bridge', 'Bridge edited', 'Bridge edited successfully: ' + str(bridge), 'INFO')
            return responce
        except Exception as e:
            logger.log('edit_bridge', 'Error editing bridge', str(e), 'ERROR')
            responce['status'] = 'error'
            responce['message'] = 'Error editing bridge ' + str(e)
            return responce
            
    def delete_bridge(self, bridge_id):
        responce = {}
        try:
            bridge = HueBridge.get_by_id(bridge_id)
            bridge.delete_instance()
            responce['status'] = 'success'
            responce['message'] = 'Bridge deleted'
            logger.log('delete_bridge', 'Bridge deleted', 'Bridge deleted successfully: ' + str(bridge), 'INFO')
            return responce
        except Exception as e:
            logger.log('delete_bridge', 'Error deleting bridge', str(e), 'ERROR')
            responce['status'] = 'error'
            responce['message'] = 'Error deleting bridge ' + str(e)
            return responce