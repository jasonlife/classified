# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-25 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thoughts', '0002_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(upload_to=b''),
        ),
    ]
