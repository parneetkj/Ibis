# Generated by Django 4.1.3 on 2022-11-23 12:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='duration',
            field=models.IntegerField(choices=[(15, '15 Minute'), (30, '30 Minute'), (45, '45 Minute'), (60, '1 Hour')], default=30),
        ),
        migrations.AlterField(
            model_name='request',
            name='time',
            field=models.TimeField(default=datetime.time(12, 2, 50, 515502)),
        ),
    ]