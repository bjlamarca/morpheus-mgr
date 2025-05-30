
from peewee import *
from devices.models import DeviceType, Device

hue_db_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = hue_db_proxy

class HueBridge(BaseModel):
    username = CharField()
    ip_addr = CharField()
    key = CharField()
    name = CharField()
    active = BooleanField(default=True)

class HueDevice(BaseModel):
    device_type = ForeignKeyField(model=DeviceType, backref='hue_devices')
    device = ForeignKeyField(model=Device, backref='hue_devices', on_delete='SET NULL', null=True)
    bridge = ForeignKeyField(model=HueBridge, backref='hue_devices')
    hue_id = CharField()
    model_id = CharField()
    manufacturer_name = CharField()
    product_name = CharField()
    software_version = CharField()
    name = CharField()
    zigbee_rid = CharField()
    power_rid = CharField(null=True)
    bridge_rid = CharField(null=True)
    online = BooleanField(null=True)
    updated = DateTimeField(null=True)
    battery_level = IntegerField(null=True)
    morph_sync = BooleanField()
    
    def __str__(self):
        return self.name
    
class HueLight(BaseModel):
    device = ForeignKeyField(model=HueDevice, on_delete='CASCADE'),
    rid = CharField()
    switch = CharField(null=True) #on or off
    dimming = IntegerField(null=True)
    gamut_type = CharField()
    red = IntegerField(null=True)
    green = IntegerField(null=True)
    blue = IntegerField(null=True)
    effect = CharField(null=True)
    
    def __str__(self):
        return self.rid
    
class HueButton(BaseModel):
    device = ForeignKeyField(model=HueDevice, backref='hue_buttons')
    rid = CharField()
    name = CharField()
    updated = DateTimeField(null=True)
    event = CharField(null=True)
    
    def __str__(self):
        return self.name
    

def update_hue_tables():
    db = hue_db_proxy
    db.connect()
    db.create_tables([HueBridge, HueDevice, HueLight, HueButton])
    db.close()
    print('Hue tables updated')