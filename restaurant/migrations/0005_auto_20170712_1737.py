# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-12 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_auto_20170712_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant_profile',
            name='tables_count',
            field=models.CharField(max_length=3),
        ),
    ]