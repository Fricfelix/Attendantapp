# Generated by Django 4.1.5 on 2023-03-20 11:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create', '0004_alter_officeattendancecreationmodel_attendance_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officeattendancecreationmodel',
            name='attendance_duration',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 21, 11, 22, 45, 196949, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='studentattendancecreationmodel',
            name='attendance_duration',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 21, 11, 22, 45, 181328, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
