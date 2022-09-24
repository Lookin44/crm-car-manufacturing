from django.db import models

from .user import CustomUser


class DowntimeType(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Downtime type'
        verbose_name_plural = 'Downtime types'

    def __str__(self):
        return self.name


class Downtime(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='downtimes',
        null=True,
        blank=True
    )
    downtime_type = models.ForeignKey(
        DowntimeType,
        on_delete=models.SET_NULL,
        related_name='downtimes',
        null=True,
        blank=True
    )
    time_start = models.DateTimeField(editable=True)
    time_amount = models.PositiveIntegerField()
    comment = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Downtime'
        verbose_name_plural = 'Downtimes'

    def __str__(self):
        return self.downtime_type.name
