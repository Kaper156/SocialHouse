from django.contrib import admin

# Register your models here.
from .models import Meter, MeterData, SealingMeter, UtilityBil

admin.site.register(Meter)
admin.site.register(MeterData)
admin.site.register(SealingMeter)
admin.site.register(UtilityBil)
