# Generated by Django 4.1.3 on 2022-11-24 22:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='date',

            field=models.DateField(default=datetime.datetime(2022, 11, 24, 22, 47, 39, 565751, tzinfo=datetime.timezone.utc)),

        ),
        migrations.AlterField(
            model_name='request',
            name='time',

            field=models.TimeField(default=datetime.datetime(2022, 11, 24, 22, 47, 39, 565772, tzinfo=datetime.timezone.utc)),

        ),
    ]
