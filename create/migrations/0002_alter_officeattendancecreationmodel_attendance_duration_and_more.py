# Generated by Django 4.2.7 on 2023-11-11 12:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officeattendancecreationmodel',
            name='attendance_duration',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 12, 12, 21, 14, 250196, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='studentattendancecreationmodel',
            name='attendance_duration',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 12, 12, 21, 14, 245196, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
