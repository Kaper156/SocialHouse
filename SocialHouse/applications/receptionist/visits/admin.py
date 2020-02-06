from django.contrib import admin

# Register your models here.
from .models import Visit, Visitor

admin.site.register(Visit)
admin.site.register(Visitor)
