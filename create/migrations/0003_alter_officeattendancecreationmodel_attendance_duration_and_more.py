# Generated by Django 4.2.7 on 2023-11-16 21:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create', '0002_alter_officeattendancecreationmodel_attendance_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officeattendancecreationmodel',
            name='attendance_duration',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 17, 21, 5, 11, 357118, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='studentattendancecreationmodel',
            name='attendance_duration',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 17, 21, 5, 11, 357118, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
