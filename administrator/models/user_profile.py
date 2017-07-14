# -*- coding: utf-8 -*-
"""
Allows to create a user in a database.

Contains a model class for users and a manager for this model.

:copyright: (c) 2017 by Ol'ha Leskovs'ka
"""

import ConfigParser
import os

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    """Manages creation of users in a database.

    Methods:
    create_user -- for users creation
    create_superuser -- for superuser creation
    """

    def _create_user(self, email, name, password, **extra_fields):
        """Creates, saves and returns a user.

        Arguments:
        email - user's email
        name - user's name
        password - user's password
        extra_fields - any other fields
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password, **extra_fields):
        """Creates and saves an ordinary user with the given email,
        name and password.

        Arguments:
        email - user's email
        name - user's name
        password - user's password
        extra_fields - any other fields
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, password, **extra_fields)

    def create_superuser(self, email, name, password, **extra_fields):
        """Creates and saves a superuser with the given email,
        name and password.

        Arguments:
        email - user's email
        name - user's name
        password - user's password
        extra_fields - any other fields
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):

    """Implements a fully featured User model and handles data about
    users in DB.

    Extends AbstractBaseUser class with such fields as status and
    avatar. Except this the email is used as the username filed when
    users login.

    Methods:
    get_short_name - returns an email
    def email_to_user - sends a letter to the user

    Fields:
    name - user's name
    email - user's email
    password - user's password
    phone - user's phone
    avatar - user's avatar
    status - user's status
    is_staff - if user has admin's permissions
    is_active - if user is active

    Email and password are required. Other fields are optional.
    """

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # set directory with outlying configuration files

    CONF_ROOT = os.path.join(BASE_DIR, 'configurations')

    CONF_FILE = (os.path.join(CONF_ROOT, 'config.ini'))

    config = ConfigParser.ConfigParser()
    config.read(CONF_FILE)

    ACTIVE = config.getint('USER_STATUSES', 'ACTIVE')
    DELETED = config.getint('USER_STATUSES', 'DELETED')
    BANNED = config.getint('USER_STATUSES', 'BANNED')
    UNAUTHORIZED = config.getint('USER_STATUSES', 'UNAUTHORIZED')

    USER_STATUSES = (
        (ACTIVE, 'active'),
        (DELETED, 'deleted'),
        (BANNED, 'banned'),
        (UNAUTHORIZED, 'unauthorized'),
    )

    #Fields
    name = models.CharField(max_length=50, default='')
    email = models.EmailField(_('email address'), unique=True, default='',
                              error_messages={'unique': _("A user with such"
                                                          " email already "
                                                          "exists."), })
    password = models.CharField(max_length=128, blank=True, default='')
    phone = models.CharField(max_length=12, blank=True, null=True,
                             unique=True)
    avatar = models.ImageField(upload_to='user_images', blank=True, null=True)
    status = models.IntegerField(choices=USER_STATUSES, default='0')
    is_staff = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    #End fields

    objects = UserManager()

    USERNAME_FIELD = 'email'

    #A list of the field names that will be prompted for when creating
    #  a user via the createsuperuser  management command
    REQUIRED_FIELDS = ['name']

    class Meta():
        """Gives some options (metadata) attached to the model."""
        db_table = "users"
        verbose_name = ('user')

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def email_to_user(self, subject, message, sender=None, **kwargs):
        """Sends an email to the user

        Arguments:
        subject - a theme of the letter
        message - a message of the email
        sender - a sender/author of the email
        **kwargs - other arguments
        """
        send_mail(subject, message, sender, [self.email], **kwargs)
