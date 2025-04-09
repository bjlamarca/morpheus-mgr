class Signal():
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls.handlers = []
            cls._instance = super().__new__(cls)
        
        return cls._instance
    
    def __init__(cls):
        pass
        #print('Signal created', cls.handlers)

    def connect(cls, group, handler):
        cls.handlers.append([group, handler])
        #print('Signal connected', cls.handlers)

    def disconnect(cls, handler):
        cls.handlers.remove(handler)
        #print('Signal disconnected')

    def send(cls, group, sender, data_dict, local_only=False):
        #print('Signal sent', group, sender, data_dict)
        for handler in cls.handlers:
            if handler[0] == group:
                handler[1](sender,  data_dict)

    