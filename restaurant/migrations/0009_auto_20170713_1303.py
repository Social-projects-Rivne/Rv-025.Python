# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-13 10:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0008_remove_restaurant_profile_is_deleted'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Restaurant_profile',
            new_name='Restaurant',
        ),
        migrations.RenameModel(
            old_name='Restaurant_type',
            new_name='RestaurantType',
        ),
    ]