from django.contrib import admin

from applications.department.people.models import Visitor
from .models import Visit

admin.site.register(Visit)
admin.site.register(Visitor)
