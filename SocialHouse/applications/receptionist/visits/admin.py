from django.contrib import admin

from applications.people.models import Visitor
# Register your models here.
from .models import Visit

admin.site.register(Visit)
admin.site.register(Visitor)
