from peewee import *

sys_db_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = sys_db_proxy

class Hub(BaseModel):
    name = CharField()
    ip_address = CharField(null=True)
    mac_address = CharField(null=True)
    last_seen = DateTimeField(null=True)
    primary = BooleanField(default=True)
    connected_hub = ForeignKeyField(model='self', backref='secondary_hubs', on_delete='SET NULL', null=True)
    
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

def update_sys_tables():
    db = sys_db_proxy
    db.connect()
    db.create_tables([Hub, ColorFamily, Color, SystemLog, ColorColorFamily])
    db.close()
    print('System tables updated')
    return True