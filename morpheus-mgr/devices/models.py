from peewee import *

device_db_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = device_db_proxy

class Room(BaseModel):
    name = CharField()

    def __str__(self):
        return self.name

class DeviceType(BaseModel):
    name = CharField()
    display_name = CharField()
    interface = CharField(null=True)
    capability = CharField(null=True)

    def __str__(self):
        return self.display_name

class Device(BaseModel):
    name = CharField()
    device_object_id = BigIntegerField()
    device_type = ForeignKeyField(model=DeviceType, backref='devices')
    room = ForeignKeyField(model=Room, backref='devices', on_delete='SET NULL', null=True)
    
    def __str__(self):
        return self.name