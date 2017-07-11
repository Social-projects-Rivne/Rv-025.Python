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

from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    def _create_user(self, email, name, password, **extra_fields):
        """Creates and saves a User with the given email, name and password."""

        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, password, **extra_fields)

    def create_superuser(self, email, name, password, **extra_fields):
        """Creates and saves a superuser with the given email, name and password."""

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, password, **extra_fields)



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
    name = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), unique=True, default='mail',
                              error_messages={
                                  'unique': _("A user with such email already exists."), })
    password = models.CharField(max_length=128, default='pass')
    phone = models.CharField(max_length=12, null=True, unique=True)
    avatar = models.ImageField(upload_to='user_images', blank=True, null=True)
    status = models.IntegerField(choices=USER_STATUSES, default='3')
    is_staff = models.BooleanField(default=False, null=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta():
        """This class gives some options (metadata) attached to the model."""
        db_table = "users"
        verbose_name = ('user')

    def get_short_name(self):
        """Returns the name of the user"""
        return self.name

    def email_to_user(self, subject, message, sender=None, **kwargs):
        """Sends an email to the user"""
        send_mail(subject, message, sender, [self.email], **kwargs)