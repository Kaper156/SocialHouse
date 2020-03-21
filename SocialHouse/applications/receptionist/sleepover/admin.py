from django.contrib import admin

# Register your models here.
from .models import NightShift, ServicedPersonOvernight, VisitorOvernight

admin.site.register(NightShift)
admin.site.register(ServicedPersonOvernight)
admin.site.register(VisitorOvernight)
