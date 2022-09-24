from django.db import models

from .common import Shift, Zone
from .rotation import Station
from .user import CustomUser


class Subpoint(models.Model):
    question = models.CharField(max_length=256)
    answer = models.BooleanField(null=True, default=None)
    comment = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Subpoint'
        verbose_name_plural = 'Subpoints'

    def __str__(self):
        return f'{self.question[:15]} - {self.answer[:15]}'


class Action(models.Model):
    deviation = models.CharField(max_length=256)
    implemented_action = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'

    def __str__(self):
        return f'{self.deviation[:15]} - {self.implemented_action[:15]}'


class CarModel(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'CarModel'
        verbose_name_plural = 'CarModels'

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipments'

    def __str__(self):
        return self.name


class OperationTimeAnalysis(models.Model):
    standart_operating_time = models.FloatField()
    measured_time = models.FloatField()
    steps_amount = models.PositiveIntegerField()
    take_amount = models.PositiveIntegerField()
    put_amount = models.PositiveIntegerField()
    waiting = models.FloatField()
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.SET_NULL,
        related_name='operation_time_analysis',
        null=True,
        blank=True
    )
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.SET_NULL,
        related_name='operation_time_analysis',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'OperationTimeAnalysis'
        verbose_name_plural = 'OperationTimeAnalysis'

    def __str__(self):
        return self.name


class JobObservation(models.Model):
    date_observation = models.DateTimeField()
    focus = models.CharField(max_length=256)
    impovements = models.CharField(max_length=256)
    signature = models.BooleanField(default=False)
    zone = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        related_name='job_observations',
        null=True,
        blank=True
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.SET_NULL,
        related_name='job_observations',
        null=True,
        blank=True
    )
    observer_user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='observers',
        null=True,
        blank=True
    )
    station = models.ForeignKey(
        Station,
        on_delete=models.SET_NULL,
        related_name='job_observations',
        null=True,
        blank=True
    )
    operator_user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='operators',
        null=True,
        blank=True
    )
    subpoint = models.ManyToManyField(
        Subpoint,
        related_name='job_observations',
        through='SubpointJobObservation',
        through_fields=('subpoint', 'job_observation')
    )
    operational_time_analysis = models.ManyToManyField(
        OperationTimeAnalysis,
        related_name='job_observations',
        through='TimeAnalysisJobObservation',
        through_fields=('time_analysis', 'job_observation')
    )
    comment_senior_supervisor = models.CharField(
        max_length=256,
        default=None,
        blank=True,
        null=True
    )
    action = models.ManyToManyField(
        Action,
        related_name='job_observations',
        through='ActionJobObservation',
        through_fields=('action', 'job_observation')
    )


class SubpointJobObservation(models.Model):
    subpoint = models.ForeignKey(
        Subpoint,
        on_delete=models.CASCADE,
        related_name='subpoint_job_observation'
    )
    job_observation = models.ForeignKey(
        JobObservation,
        on_delete=models.CASCADE,
        related_name='subpoint_job_observation'
    )

    class Meta:
        verbose_name = 'SubpointJobObservation'
        verbose_name_plural = 'SubpointJobObservations'

    def __str__(self):
        return self.job_observation.date_observation


class TimeAnalysisJobObservation(models.Model):
    time_analysis = models.ForeignKey(
        OperationTimeAnalysis,
        on_delete=models.CASCADE,
        related_name='time_analysis_job_observation'
    )
    job_observation = models.ForeignKey(
        JobObservation,
        on_delete=models.CASCADE,
        related_name='time_analysis_job_observation'
    )

    class Meta:
        verbose_name = 'TimeAnalysisJobObservation'
        verbose_name_plural = 'TimeAnalysisJobObservations'

    def __str__(self):
        return self.job_observation.date_observation


class ActionJobObservation(models.Model):
    action = models.ForeignKey(
        Action,
        on_delete=models.CASCADE,
        related_name='action_job_observation'
    )
    job_observation = models.ForeignKey(
        JobObservation,
        on_delete=models.CASCADE,
        related_name='action_job_observation'
    )

    class Meta:
        verbose_name = 'ActionJobObservation'
        verbose_name_plural = 'ActionJobObservations'

    def __str__(self):
        return self.job_observation.date_observation
