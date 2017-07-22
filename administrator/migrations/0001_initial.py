# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 09:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(default=b'', help_text='50 characters or fewer.', max_length=50)),
                ('email', models.EmailField(default=b'', error_messages={b'unique': 'A user with such email already exists.'}, max_length=254, unique=True, verbose_name='email address')),
                ('password', models.CharField(default=b'', help_text="Your password can't be too similar to your other personal information.<br /> Your password must contain at least 8 characters.<br /> Your password can't be a commonly used password.<br /> Your password can't be entirely numeric.", max_length=128)),
                ('phone', models.CharField(blank=True, help_text="Use just numbers: '380931234567", max_length=12, null=True, unique=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=b'user_images')),
                ('role', models.IntegerField(choices=[(0, b'user'), (1, b'admin'), (3, b'manager'), (4, b'submanager')], default=0)),
                ('status', models.IntegerField(choices=[(0, b'active'), (1, b'deleted'), (3, b'banned'), (4, b'unauthorized')], default=0)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
                'permissions': (('read_user', 'Can read information about user'),),
            },
        ),
    ]
