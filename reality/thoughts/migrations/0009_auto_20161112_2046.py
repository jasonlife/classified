# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-12 20:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('thoughts', '0008_auto_20161112_2039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bella',
            name='name',
        ),
        migrations.RemoveField(
            model_name='bella',
            name='slug',
        ),
        migrations.AddField(
            model_name='bella',
            name='content',
            field=models.CharField(default=datetime.datetime(2016, 11, 12, 20, 46, 56, 81877, tzinfo=utc), max_length=1500),
            preserve_default=False,
        ),
    ]
