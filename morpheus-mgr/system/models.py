from peewee import *
from system.server import ServerManger


server_manager = ServerManger()
db = server_manager.db

class BaseModel(Model):
    class Meta:
        database = db


class Room(BaseModel):
    name =CharField()

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


class ColorFamily(BaseModel):
    name = CharField()

    def __str__(self):
        return self.name
    
class Color(BaseModel):
    name = CharField()
    favorite = BooleanField()
    hex_code = CharField()
    red = IntegerField()
    green = IntegerField()
    blue = IntegerField()
    color_family = ManyToManyField(ColorFamily, backref='colors')
    sort = IntegerField(null=True)
   

    def __str__(self):
        return self.name
    
ColorColorFamily = Color.color_family.get_through_model()

class SystemLog(BaseModel):
    date_time = DateTimeField(null=True)
    module = CharField(null=True)
    method = CharField(null=True)
    message = CharField(null=True)
    details = CharField(null=True)
    level = CharField(null=True)    

def update_db():
    db.connect()
    db.create_tables([Room, DeviceType, Device, ColorFamily, Color, ColorColorFamily, SystemLog])
    db.close()
    print('Database connection successful')
    return True