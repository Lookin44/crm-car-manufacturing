from django.db import models


class Zone(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Zone'
        verbose_name_plural = 'Zones'

    def __str__(self):
        return self.name


class Shift(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name = 'Shift'
        verbose_name_plural = 'Shifts'

    def __str__(self):
        return self.name
