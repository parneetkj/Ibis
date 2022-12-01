# Generated by Django 4.1.3 on 2022-12-01 12:50

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('is_student', models.BooleanField(default=False, verbose_name='student status')),
                ('is_admin', models.BooleanField(default=False, verbose_name='admin status')),
                ('is_director', models.BooleanField(default=False, verbose_name='director status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2022, 12, 1, 12, 50, 54, 553704, tzinfo=datetime.timezone.utc))),
                ('time', models.TimeField(default=datetime.datetime(2022, 12, 1, 12, 50, 54, 553730, tzinfo=datetime.timezone.utc))),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1, message='Must book at least 1 lesson.'), django.core.validators.MaxValueValidator(limit_value=50, message='Cannot book more than 50 lessons.')])),
                ('interval', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1, message='Must book at least 1 week of lessons.'), django.core.validators.MaxValueValidator(limit_value=4, message='Interval cannot be more than a month.')])),
                ('duration', models.IntegerField(choices=[(15, '15 Minute'), (30, '30 Minute'), (45, '45 Minute'), (60, '1 Hour')], default=30)),
                ('topic', models.CharField(blank=True, default='Any', max_length=50)),
                ('teacher', models.CharField(blank=True, default='Any', max_length=100)),
                ('status', models.CharField(default='In Progress', max_length=20)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=10)),
                ('time', models.TimeField()),
                ('start_date', models.DateField()),
                ('duration', models.IntegerField(choices=[(15, '15 Minute'), (30, '30 Minute'), (45, '45 Minute'), (60, '1 Hour')], default=30)),
                ('interval', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1, message='Must book at least 1 week of lessons.'), django.core.validators.MaxValueValidator(limit_value=4, message='Interval cannot be more than a month.')])),
                ('teacher', models.CharField(max_length=100)),
                ('no_of_lessons', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1, message='Must book at least 1 lesson.'), django.core.validators.MaxValueValidator(limit_value=50, message='Cannot book more than 50 lessons.')])),
                ('topic', models.CharField(max_length=50)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
