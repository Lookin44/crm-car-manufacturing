from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (Action, ActionJobObservation, CarModel, CustomUser,
                     Downtime, DowntimeType, Equipment, JobObservation,
                     OperationTimeAnalysis, Position, Rotation, Shift, Station,
                     Subpoint, SubpointJobObservation,
                     TimeAnalysisJobObservation, Training, UserTraining, Zone)


class TrainingInline(admin.TabularInline):
    model = CustomUser.training.through
    extra = 0


class ActionInline(admin.TabularInline):
    model = JobObservation.action.through
    extra = 0


class OperationTimeAnalysisInline(admin.TabularInline):
    model = JobObservation.operational_time_analysis.through
    extra = 0


class SubpointInline(admin.TabularInline):
    model = JobObservation.subpoint.through
    extra = 0


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description')


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('pk', 'letter_designation')


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
    inlines = (TrainingInline, )
    exclude = ('training', 'groups', 'user_permissions')


@admin.register(JobObservation)
class JobObservationAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'date_observation',
        'focus',
        'improvement',
        'signature',
        'zone',
        'shift',
        'observer_user',
        'station',
        'operator_user',
        'comment_senior_supervisor'
    )
    inlines = (ActionInline, SubpointInline, OperationTimeAnalysisInline)
    exclude = ('action', 'subpoint', 'operational_time_analysis')


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
        'downtime_type',
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


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'deviation', 'implemented_action')


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(OperationTimeAnalysis)
class OperationTimeAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'standard_operating_time',
        'measured_time',
        'steps_amount',
        'take_amount',
        'put_amount',
        'waiting',
        'car_model',
        'equipment'
    )


@admin.register(Subpoint)
class SubpointAdmin(admin.ModelAdmin):
    list_display = ('pk', 'question', 'answer', 'comment')


@admin.register(SubpointJobObservation)
class SubpointJobObservationAdmin(admin.ModelAdmin):
    list_display = ('subpoint', 'job_observation')


@admin.register(TimeAnalysisJobObservation)
class TimeAnalysisJobObservationAdmin(admin.ModelAdmin):
    list_display = ('time_analysis', 'job_observation')


@admin.register(ActionJobObservation)
class ActionJobObservationAdmin(admin.ModelAdmin):
    list_display = ('action', 'job_observation')


admin.site.unregister(Group)
