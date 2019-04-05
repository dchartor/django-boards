from django.contrib import admin
from . import models


class BoardAdmin(admin.ModelAdmin):
    search_fields = ['title']


class PostAdmin(admin.ModelAdmin):
    list_display = ('topic')
    list_filter = ['created_at']
    date_hierarchy = 'created_at'


admin.site.register(models.Board)
admin.site.register(models.Topic)
admin.site.register(models.Post)
