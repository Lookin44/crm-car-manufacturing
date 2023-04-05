from django.db import models


class Zone(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256)
    shop = models.ForeignKey(
        'Shop',
        on_delete=models.SET_NULL,
        related_name='zones',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Zone'
        verbose_name_plural = 'Zones'

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

    def __str__(self):
        return self.name


class Shift(models.Model):
    letter_designation = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name = 'Shift'
        verbose_name_plural = 'Shifts'

    def __str__(self):
        return self.letter_designation
