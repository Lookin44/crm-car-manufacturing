from django.contrib.auth.models import AbstractUser
from django.db import models

from ..api.models.common import Shift, Zone


class Position(models.Model):
    name = models.CharField(max_length=256, unique=True)
    grade = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    patronymic = models.CharField(max_length=256)
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True
    )
    zone = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
