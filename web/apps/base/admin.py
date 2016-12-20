from django.contrib import admin
from base.models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ('author', 'file', 'category', 'tags')

admin.site.register(Image, ImageAdmin)
