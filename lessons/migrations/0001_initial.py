# Generated by Django 4.1.3 on 2022-11-12 14:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.CharField(max_length=50)),
                ('availability', models.CharField(max_length=200)),
                ('amount', models.IntegerField(validators=[django.core.validators.MinLengthValidator(limit_value=1, message='Must book at least 1 lesson.'), django.core.validators.MaxLengthValidator(limit_value=50, message='Cannot book more than 50 lessons.')])),
                ('interval', models.IntegerField(validators=[django.core.validators.MinLengthValidator(limit_value=1, message='Must book at least 1 week of lessons.'), django.core.validators.MaxLengthValidator(limit_value=4, message='Interval cannot be more than a month.')])),
                ('duration', models.IntegerField(choices=[(15, '15 Minuite'), (30, '30 Minuite'), (45, '45 Minuite'), (60, '1 Hour')], default=30)),
                ('topic', models.CharField(default='Any', max_length=50)),
                ('teacher', models.CharField(default='Any', max_length=100)),
            ],
        ),
    ]
