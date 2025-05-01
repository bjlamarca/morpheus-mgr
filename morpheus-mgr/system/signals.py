

class Signal():
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls.handlers = []
            cls._instance = super().__new__(cls)
            from system.hub import HubSocket
            cls.socket = HubSocket()
        
        return cls._instance
    
    def __init__(cls):
        pass
        #print('Signal created', cls.handlers)

    def connect(cls, handler, area_list=None):
        cls.handlers.append([area_list, handler])
        #print('Signal connected', cls.handlers)

    def disconnect(cls, handler):
        cls.handlers.remove(handler)
        #print('Signal disconnected')

    def send(cls, sender, data_dict, local_only=False):
        #print('Signal sent', group, sender, data_dict)
        area = data_dict['area']
        for handler in cls.handlers:
            if handler[0]:
                if area in handler[0]:
                    handler[1](sender,  data_dict)
                
        if local_only == False:
            cls.socket.send(data_dict)
            #print('Signal sent to socket', data_dict)

    