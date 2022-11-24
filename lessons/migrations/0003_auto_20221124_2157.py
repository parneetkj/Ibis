# Generated by Django 3.2.12 on 2022-11-24 21:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_alter_request_date_alter_request_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 11, 24, 21, 57, 33, 826146, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='request',
            name='time',
            field=models.TimeField(default=datetime.datetime(2022, 11, 24, 21, 57, 33, 826175, tzinfo=utc)),
        ),
    ]
