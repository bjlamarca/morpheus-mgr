class Room(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Name',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('devices:device-room', args=[self.pk])
    

class DeviceType(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Name'
    )
    display_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Display Name'
    )
    interface_device_type = models.CharField(
        max_length=100,
        verbose_name='Interface Display Name'
    )
    interface = models.CharField(
        max_length=100,
        verbose_name='Interface'
    )
    capability = models.CharField(
        max_length=500,
        verbose_name='Capabilities'
    )

    def __str__(self):
        return self.display_name

    def get_absolute_url(self):
        return reverse('devices:devicetype', args=[self.pk])
    
    
class Device(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Name'
    )

    device_content_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Content Type'
    )
    device_object_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name='Content Object ID'
    )

    device_content_object = GenericForeignKey(
        'device_content_type',
        'device_object_id',
    
        
    )
    device_type = models.ForeignKey(
        DeviceType,
        on_delete = models.SET_NULL,
        verbose_name='Device Type',
        blank=True,
        null=True
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        verbose_name='Room', 
        blank=True,
        null=True   
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('devices:device-detail', args=[self.pk])
    
    @property
    def interface_name(self):
        return (self.device_content_type.app_label).capitalize()

class ColorFamily(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Name'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('devices:colorfamily', args=[self.pk])

class Color(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Name'
    )
    favorite = models.BooleanField(
        verbose_name='Favorite'
    )
    hex_code = models.CharField(
        max_length=7,
        verbose_name='Hex Code'
    )
    red = models.IntegerField(
        verbose_name='Red'
    )
    green = models.IntegerField(
        verbose_name='Green'
    )
    blue = models.IntegerField(
        verbose_name='Blue'
    )
    color_family = models.ManyToManyField(
        ColorFamily,
        verbose_name='Color Family'
    )
    sort = models.IntegerField(
        verbose_name='Sort',
        blank=True,
        null=True
    )    


    def __str__(self):
        return self.name



HUE_DEVICE_TYPE = [
        ['WHITELAMP', 'White Lamp'],
        ['COLORLAMP', 'Color Lamp'],
        ['DIMSWITCH', 'Dimmer Switch'],
        ['HUB', 'Hue Hub']
    ]

class HueDevice(models.Model):
    #Morpheus categorization of Hue devices  
    hue_device_type = models.CharField(
        max_length=100,
        blank=True,
        choices=HUE_DEVICE_TYPE,
        verbose_name='Hue Device Type'
    )
    hub_id = models.IntegerField(
        blank=False,
        verbose_name='Hub ID'
    )
    hue_id = models.CharField(
        max_length=100,
        verbose_name='Hue ID'
    )
    hue_id_v1 = models.CharField(
        max_length=100
    )
    model_id = models.CharField(
        max_length=100,
        verbose_name='Model ID'
    )
    manufacturer_name = models.CharField(
        max_length=100,
        verbose_name='Manufacture Name'
    )
    product_name = models.CharField(
        max_length=100,
        verbose_name='Product Name'

    )
    software_version = models.CharField(
        max_length=100,
        verbose_name='Software Version'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Name'

    )
    zigbee_rid = models.CharField(
        max_length=100,
        verbose_name='ZigBee RID'

    )
    power_rid = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Power RID'
    )
    bridge_rid = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Bridge RID'
    )
    online = models.BooleanField(
        blank=True,
        null=True,
        default=True,
        verbose_name='Online'
    )
    last_checkin = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Last Check-in'
        
    )
    battery_level = models.IntegerField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Battery Level'
    )
    morph_sync = models.BooleanField(  
        default=False,
        verbose_name='Sync to Devices'
    )
    class Meta:
        verbose_name = 'Hue Device'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hue:device', args=[self.pk])

SWITCH_CHOICES = [
    ['on', 'On'],
    ['off', 'Off']
]

class HueLight(models.Model):
    
    device = models.ForeignKey(
        HueDevice,
        on_delete = models.CASCADE,
        verbose_name='Device'
    )
    rid = models.CharField(
        max_length=100,
        verbose_name='RID'
    )
    light_on = models.BooleanField(
        blank=True,
        null=True,
        verbose_name='Light On'
    )
    switch = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=SWITCH_CHOICES,
        verbose_name='Switch'
    )
    dimming = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Dimming'
        )
    gamut_type = models.CharField(max_length=50,
        blank=True,
        null=True,
        verbose_name='Gamut Type'
        )
    red = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Red'
        )
    green = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Green'
        )
    blue = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Blue'
        )
    effect = models.CharField(max_length=50,
        blank=True,
        null=True,
        verbose_name='Effect'
    )

    class Meta:
        verbose_name = 'Hue Light'

    def __str__(self):
        return self.rid

    def get_absolute_url(self):
        return reverse('hue:light', args=[self.pk])
        
class HueButton(models.Model):
    device = models.ForeignKey(
        HueDevice,
        on_delete = models.CASCADE,
        verbose_name='Device'
    )
    rid = models.CharField(
        max_length=100,
        verbose_name='RID'
    )
    name = models.CharField(
        max_length=300,
        verbose_name='Name'
    )
    updated = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Last Update'
    )
    event = models.CharField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Last Event'
    )
    

    class Meta:
        verbose_name = 'Hue Buttons'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hue:light', args=[self.pk])



####Scene

class Scene(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Name'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('scenes:detail', args=[self.pk])

SWITCH_CHOICES = [
    ['on', 'On'],
    ['off', 'Off']
] 

class SceneDevices(models.Model):
    
    scene = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        verbose_name='Device'
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        verbose_name='Device'
    )
    scene_device_capability = models.CharField(
        max_length=500,
        verbose_name='Capabilities',
        blank=True,
        null=True,
    )
    light_on = models.BooleanField(
        blank=True,
        null=True,
        verbose_name='Light On'
    )
    switch = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=SWITCH_CHOICES,
        verbose_name='Switch'
    )
    dimming = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Dimming'
        )
    red = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Red'
        )
    green = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Green'
        )
    blue = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Blue'
        )


#### Tiles

class Page(models.Model):
    name = models.CharField(max_length=100)
    page_type = models.CharField(
        max_length=100,
        choices=page_types.get_page_types_choices(),
    )

    def __str__(self):
        return self.name

class PageSection(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
        )
    page = models.ForeignKey(
        Page, 
        on_delete=models.CASCADE
    )
    sort = models.IntegerField()
    
    def __str__(self):
        return self.name
    
class Tile(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
        )
    page_section = models.ForeignKey(
        PageSection, 
        on_delete=models.CASCADE
    )
    tile_type = models.CharField(
        max_length=100,
        choices=tile_types.get_tile_types_choices(),
       )
    tile_object_id = models.IntegerField()   
    
    sort = models.IntegerField()


 
    



