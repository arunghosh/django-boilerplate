# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('field_name_2', models.CharField(max_length=10, null=True, blank=True)),
                ('field_name_1', models.CharField(max_length=10, null=True, blank=True)),
                ('user', models.OneToOneField(related_name='profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=64, null=True, blank=True)),
                ('last_name', models.CharField(max_length=64, null=True, blank=True)),
                ('email', models.CharField(max_length=128)),
                ('mobile', models.CharField(max_length=64, null=True, blank=True)),
                ('gender', models.PositiveSmallIntegerField(default=0, verbose_name=b'Gender', choices=[(0, b'--'), (1, b'Male'), (2, b'Female'), (3, b'Other')])),
                ('dob', models.DateField(null=True, blank=True)),
                ('user_type', model_utils.fields.StatusField(default=b'staff', max_length=100, no_check_for_status=True, choices=[(b'profile1', b'profile1'), (b'profile2', b'profile2'), (b'staff', b'staff')])),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Joined On')),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile1Proxy',
            fields=[
            ],
            options={
                'verbose_name': 'Profile1',
                'proxy': True,
            },
            bases=('profiles.profile',),
        ),
        migrations.CreateModel(
            name='Profile2Proxy',
            fields=[
            ],
            options={
                'verbose_name': 'Profile2',
                'proxy': True,
            },
            bases=('profiles.profile',),
        ),
    ]
