from django.contrib import admin

from .models.common import Zone, Shift
from .models.training import Training


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description')


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'date_first', 'date_last')
