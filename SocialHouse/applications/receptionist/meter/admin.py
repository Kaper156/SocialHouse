from django.contrib import admin

# Register your models here.
from .models import Meter, MeterData, SealingMeter

admin.site.register(Meter)
admin.site.register(MeterData)
admin.site.register(SealingMeter)
