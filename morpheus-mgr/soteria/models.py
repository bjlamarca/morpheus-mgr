from peewee import *
from devices.models import DeviceType, Device


soteria_db_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = soteria_db_proxy

class SoteriaDevice(BaseModel):
    device_type = ForeignKeyField(model=DeviceType, backref='soteria_devices')
    device = ForeignKeyField(model=Device, backref='soteria_devices', on_delete='SET NULL', null=True)
    identifier = CharField()
    name = CharField()
    ip_address = CharField(null=True)
    mac_address = CharField(null=True)
    last_seen = DateTimeField(null=True)
    supervised = BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
def update_soteria_table():
    # Create the SoteriaDevice table if it doesn't exist
    db = soteria_db_proxy
    db.connect()
    db.create_tables([SoteriaDevice])
    db.close()
    print('Soteria tables updated')
    
