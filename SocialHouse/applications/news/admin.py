from django.contrib import admin

from .models import News


class NewsAdmin(admin.ModelAdmin):
    fields = ('author',
              'title',
              'content',
              'date_of_creation',
              'date_of_update',
              'status',
              )
    readonly_fields = ('date_of_creation', 'date_of_update')


admin.site.register(News, NewsAdmin)
