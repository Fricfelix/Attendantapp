# Generated by Django 4.1.5 on 2023-03-16 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo_url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]