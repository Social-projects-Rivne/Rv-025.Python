# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-12 22:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_restaurant_profile_is_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant_profile',
            name='is_deleted',
        ),
    ]
