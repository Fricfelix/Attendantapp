# Generated by Django 4.1.5 on 2023-02-24 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create', '0009_alter_studentattendancecreationmodel_attendance_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentattendancecreationmodel',
            name='attendance_duration',
            field=models.DateTimeField(default='2023-02-25T23:07:31.184362+00:00', null=True),
        ),
    ]