# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-12 09:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_auto_20170712_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant_profile',
            name='type_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.Restaurant_type'),
        ),
    ]
