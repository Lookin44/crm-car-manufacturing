from django.contrib.auth.models import AbstractUser
from django.db import models

from .common import Shift, Zone
from .training import Training


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
        null=True,
        blank=True
    )
    zone = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True
    )
    training = models.ManyToManyField(
        Training,
        related_name='users',
        blank=True,
        through='UserTraining',
        through_fields=('user', 'training')
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class UserTraining(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='users_training'
    )
    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name='trainings_user'
    )

    class Meta:
        verbose_name = 'User training'
        verbose_name_plural = 'User trainings'

    def __str__(self):
        return self.training.name
