"""
    models.user_profile

    This module contains model class for users.
    """
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.core.mail import send_mail
from django.db import models
from django.db.models.manager import EmptyManager

from django.utils.translation import ugettext_lazy as _


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """This class is used to handle data about users in DB.

        A class implementing a fully featured User model with admin-compliant
        permissions.

        Email and password are required. Other fields are optional.
        """

    ACTIVE = 0
    DELETED = 1
    BANNED = 2
    UNAUTHORIZED = 3

    USER_STATUSES = (
        (ACTIVE, 'active'),
        (DELETED, 'deleted'),
        (BANNED, 'banned'),
        (UNAUTHORIZED, 'unauthorized'),
    )
    first_name = models.CharField(_('first name'), max_length=30, default='name')
    last_name = models.CharField(_('last name'), max_length=30, default='surname')
    email = models.EmailField(_('email address'), unique=True, default='mail',
                              error_messages={
                                  'unique': _("A user with such email already exists."), })
    password = models.CharField(max_length=128, default='pass')
    phone = models.ImageField(default=0, unique=True)
    avatar = models.ImageField(upload_to='user_images', blank=True, default='')
    status = models.IntegerField(choices=USER_STATUSES, default='3')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta():
        """This class gives some options (metadata) attached to the model."""
        db_table = "users"
        verbose_name = ('user')

    def get_full_name(self):
        """Returns the first_name and the last_name with the space in between"""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the first_name of the user"""
        return self.first_name

    def email_to_user(self, subject, message, sender=None, **kwargs):
        """Sends an email to the user"""
        send_mail(subject, message, sender, [self.email], **kwargs)