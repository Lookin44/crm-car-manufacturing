from django.contrib import admin

from .models import CustomUser, Position, TrainingUser


class TrainingUserInline(admin.TabularInline):
    model = TrainingUser
    fields = ['users', 'training']


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


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'grade')


@admin.register(TrainingUser)
class TrainingUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'training', 'user')
    list_display_links = ('training', 'user')

