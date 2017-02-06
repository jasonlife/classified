# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-12 20:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('thoughts', '0005_remove_thought_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='thought',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]