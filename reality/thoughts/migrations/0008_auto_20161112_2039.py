# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-12 20:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('thoughts', '0007_auto_20161112_2020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bella',
            name='content',
        ),
        migrations.AddField(
            model_name='bella',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bella',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2016, 11, 12, 20, 39, 6, 844544, tzinfo=utc)),
            preserve_default=False,
        ),
    ]