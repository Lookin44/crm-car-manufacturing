from django.db import models


class Training(models.Model):
    name = models.CharField(max_length=256, unique=True)
    date_first = models.DateField()
    date_last = models.DateField()

    class Meta:
        verbose_name = 'Training'
        verbose_name_plural = 'Trainings'

    def __str__(self):
        return self.name

