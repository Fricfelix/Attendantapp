# Generated by Django 4.1.5 on 2023-02-21 00:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeAttendanceCreationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.SlugField(max_length=36, unique=True)),
                ('AttendanceTitle', models.CharField(blank=True, max_length=120)),
                ('location_point_range', models.FloatField(default=100.0)),
                ('attendance_duration', models.DurationField(blank=True)),
                ('longitude', models.FloatField(null=True)),
                ('latitude', models.FloatField(null=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAttendanceCreationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.SlugField(max_length=36, unique=True)),
                ('AttendanceTitle', models.CharField(blank=True, max_length=120)),
                ('location_point_range', models.FloatField(default=100.0)),
                ('attendance_duration', models.DurationField(blank=True)),
                ('longitude', models.FloatField(null=True)),
                ('latitude', models.FloatField(null=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAttendanceTakingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('reg_number', models.CharField(max_length=120)),
                ('department', models.CharField(blank=True, max_length=200)),
                ('time_of_attendance', models.DateTimeField(default=datetime.datetime.now)),
                ('attendance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create.studentattendancecreationmodel')),
            ],
        ),
        migrations.CreateModel(
            name='OfficeAttendanceTakingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('position', models.CharField(max_length=120)),
                ('time_of_attendance', models.DateTimeField(default=datetime.datetime.now)),
                ('attendance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create.officeattendancecreationmodel')),
            ],
        ),
    ]