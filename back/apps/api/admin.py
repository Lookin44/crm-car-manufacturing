from django.contrib import admin

from .models.common import Zone, Shift


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description')


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
