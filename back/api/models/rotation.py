from django.db import models

from .user import CustomUser


class Station(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Station'
        verbose_name_plural = 'Stations'

    def __str__(self):
        return self.name


class Rotation(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True
    )
    station = models.ForeignKey(
        Station,
        on_delete=models.SET_NULL,
        related_name='stations',
        null=True,
        blank=True
    )
    date_start = models.DateTimeField()
    date_stop = models.DateTimeField()

    class Meta:
        verbose_name = 'Rotation'
        verbose_name_plural = 'Rotation'

    def __str__(self):
        return f'{self.user.username} - {self.station.name}'
