# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 09:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='restaurant',
            options={'permissions': (('read_restaurant', 'Can read information about restaurant'),), 'verbose_name': 'Restaurant'},
        ),
        migrations.AlterModelOptions(
            name='restauranttype',
            options={'permissions': (('read_restaurant', 'Can read information about restaurant'),), 'verbose_name': 'Restaurant type'},
        ),
    ]