# Generated by Django 4.1.5 on 2023-03-21 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_email_confirmation_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_confirmation_token',
            field=models.CharField(default='56191686c81511ed92f718cf5eb070a6', editable=False, max_length=36),
        ),
    ]
