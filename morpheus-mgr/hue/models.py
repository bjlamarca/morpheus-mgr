
from peewee import *
from system.models import DeviceType
from system.hub import HubManger
from system.models import DeviceType


def get_db():
    print('Hue DB called')
    hub_manager = HubManger()
    db = hub_manager.db
    return db


class BaseModel(Model):
    class Meta:
        database = get_db()

class HueBridge(BaseModel):
    username = CharField()
    ip_addr = CharField()
    key = CharField()
    name = CharField()


class HueDevice(BaseModel):
    #Morpheus categorization of Hue devices
      
    device_type = ForeignKeyField(model=DeviceType, backref='hue_devices')
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
    

def update_tables():
    db.connect()
    db.create_tables([HueBridge, HueDevice, HueLight, HueButton])
    print('Hue tables created')