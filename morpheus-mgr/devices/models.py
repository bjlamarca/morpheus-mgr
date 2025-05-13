from peewee import *
from playhouse.signals import Model, post_save

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
    
@post_save(sender=Device)
def post_save_device(sender, instance, created, **kwargs):
    if created:
        print(f"Device {instance.name} created with ID {instance.device_object_id}")
    else:
        print(f"Device {instance.name} updated with ID {instance.device_object_id}")


def update_device_tables():
    db = device_db_proxy
    db.connect()
    db.create_tables([Room, DeviceType, Device])
    db.close()
    print('Device tables updated')
    return True