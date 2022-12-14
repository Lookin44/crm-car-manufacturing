# Generated by Django 4.1.1 on 2023-01-05 20:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_station_rotation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviation', models.CharField(max_length=256)),
                ('implemented_action', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Action',
                'verbose_name_plural': 'Actions',
            },
        ),
        migrations.CreateModel(
            name='ActionJobObservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_job_observation', to='api.action')),
            ],
            options={
                'verbose_name': 'ActionJobObservation',
                'verbose_name_plural': 'ActionJobObservations',
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'CarModel',
                'verbose_name_plural': 'CarModels',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Equipment',
                'verbose_name_plural': 'Equipments',
            },
        ),
        migrations.CreateModel(
            name='JobObservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_observation', models.DateTimeField()),
                ('focus', models.CharField(max_length=256)),
                ('improvement', models.CharField(max_length=256)),
                ('signature', models.BooleanField(default=False)),
                ('comment_senior_supervisor', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('action', models.ManyToManyField(related_name='job_observations', through='api.ActionJobObservation', to='api.action')),
                ('observer_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='observers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Job observation',
                'verbose_name_plural': 'Job observations',
            },
        ),
        migrations.CreateModel(
            name='OperationTimeAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standard_operating_time', models.FloatField()),
                ('measured_time', models.FloatField()),
                ('steps_amount', models.PositiveIntegerField()),
                ('take_amount', models.PositiveIntegerField()),
                ('put_amount', models.PositiveIntegerField()),
                ('waiting', models.FloatField()),
                ('car_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operation_time_analysis', to='api.carmodel')),
                ('equipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operation_time_analysis', to='api.equipment')),
            ],
            options={
                'verbose_name': 'OperationTimeAnalysis',
                'verbose_name_plural': 'OperationTimeAnalysis',
            },
        ),
        migrations.CreateModel(
            name='Subpoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=256)),
                ('answer', models.BooleanField(default=None, null=True)),
                ('comment', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Subpoint',
                'verbose_name_plural': 'Subpoints',
            },
        ),
        migrations.AlterModelOptions(
            name='downtime',
            options={'verbose_name': 'Downtime', 'verbose_name_plural': 'Downtimes'},
        ),
        migrations.AlterModelOptions(
            name='rotation',
            options={'verbose_name': 'Rotation', 'verbose_name_plural': 'Rotation'},
        ),
        migrations.RemoveField(
            model_name='downtime',
            name='type',
        ),
        migrations.AddField(
            model_name='downtime',
            name='downtime_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='downtimes', to='api.downtimetype'),
        ),
        migrations.CreateModel(
            name='TimeAnalysisJobObservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_observation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_analysis_job_observation', to='api.jobobservation')),
                ('time_analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_analysis_job_observation', to='api.operationtimeanalysis')),
            ],
            options={
                'verbose_name': 'TimeAnalysisJobObservation',
                'verbose_name_plural': 'TimeAnalysisJobObservations',
            },
        ),
        migrations.CreateModel(
            name='SubpointJobObservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_observation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subpoint_job_observation', to='api.jobobservation')),
                ('subpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subpoint_job_observation', to='api.subpoint')),
            ],
            options={
                'verbose_name': 'SubpointJobObservation',
                'verbose_name_plural': 'SubpointJobObservations',
            },
        ),
        migrations.AddField(
            model_name='jobobservation',
            name='operational_time_analysis',
            field=models.ManyToManyField(related_name='job_observations', through='api.TimeAnalysisJobObservation', to='api.operationtimeanalysis'),
        ),
        migrations.AddField(
            model_name='jobobservation',
            name='operator_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobobservation',
            name='shift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_observations', to='api.shift'),
        ),
        migrations.AddField(
            model_name='jobobservation',
            name='station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_observations', to='api.station'),
        ),
        migrations.AddField(
            model_name='jobobservation',
            name='subpoint',
            field=models.ManyToManyField(related_name='job_observations', through='api.SubpointJobObservation', to='api.subpoint'),
        ),
        migrations.AddField(
            model_name='jobobservation',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_observations', to='api.zone'),
        ),
        migrations.AddField(
            model_name='actionjobobservation',
            name='job_observation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_job_observation', to='api.jobobservation'),
        ),
    ]
