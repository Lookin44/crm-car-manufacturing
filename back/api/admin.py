from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (
    CustomUser,
    Position,
    Shift,
    Training,
    UserTraining,
    Zone,
    DowntimeType,
    Downtime,
    Rotation,
    Station
)


class UserInline(admin.TabularInline):
    model = CustomUser.training.through
    extra = 0


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description')


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'date_first', 'date_last')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'first_name',
        'last_name',
        'patronymic',
        'position',
        'zone',
        'shift'
    )
    inlines = (UserInline, )
    exclude = ('training', 'groups', 'user_permissions')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'grade')


@admin.register(UserTraining)
class UserTrainingAdmin(admin.ModelAdmin):
    list_display = ('user', 'training')


@admin.register(DowntimeType)
class DowntimeTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description')


@admin.register(Downtime)
class DowntimeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'type',
        'time_start',
        'time_amount',
        'comment'
    )


@admin.register(Rotation)
class RotationAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'station',
        'date_start',
        'date_stop'
    )


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description')


admin.site.unregister(Group)
