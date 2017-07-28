# -*- coding: utf-8 -*-
"""
Allow to create a user in a database.
Contain a model class for users and a manager for this model.
:copyright: (c) 2017 by Ol'ha Leskovs'ka
"""

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _

from role import Role


class UserManager(BaseUserManager):

    """Manage creation of users in a database."""

    def _create_user(self, email, name, password, **extra_fields):
        """Create, save and return a user.

        Arguments:
        email - user's email
        name - user's name
        password - user's password
        extra_fields - any other fields
        Return a User object.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user.set_permissions(extra_fields.get('role'))
        return user

    def create_user(self, email, name, password, **extra_fields):
        """Create and save an ordinary user with the given email,
        name and password.

        Arguments:
        email - user's email
        name - user's name
        password - user's password
        extra_fields - any other fields
        """
        extra_fields.setdefault('role', Role.objects.get(id=2))
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, password, **extra_fields)

    def create_superuser(self, email, name, password, **extra_fields):
        """Create and save a superuser with the given email,
        name and password.

        Arguments:
        email - user's email
        name - user's name
        password - user's password
        extra_fields - any other fields
        """
        extra_fields.setdefault('role', Role.objects.get(id=1))
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    """Implement a fully featured User model and handle users data
    in DB.

    Extend AbstractBaseUser class with such fields as status and
    avatar. The email is used as the name when users login.
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

    name = models.CharField(max_length=50, default='',
                            help_text=_('50 characters or fewer.'))
    email = models.EmailField(_('email address'), unique=True, default='',
                              error_messages={'unique': _('A user with such '
                                                          'email already '
                                                          'exists.'), })
    password = models.CharField(max_length=128, default='',
                                help_text=_('Your password can\'t be too '
                                            'similar to your other personal '
                                            'information.<br /> Your password'
                                            ' must contain at least 8 '
                                            'characters.<br /> Your password '
                                            'can\'t be a commonly used '
                                            'password.<br /> Your password '
                                            'can\'t be entirely numeric.'))
    phone = models.CharField(max_length=12, blank=True, null=True,
                             unique=True, help_text=_('Use just numbers: '
                                                      ''''380931234567'''))
    avatar = models.ImageField(upload_to='user_images', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE,
                             related_name='roles', null=True)
    status = models.IntegerField(choices=USER_STATUSES, default=0, null=False)
    is_staff = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    # A list of the field names that will be prompted for when creating
    # a user via the createsuperuser management command
    REQUIRED_FIELDS = ['name']

    class Meta():

        """Give some options (metadata) attached to the model."""

        db_table = 'users'
        permissions = (
            ('read_user', 'Can read information about user'),
        )

    def set_is_active(self, status):
        """Set is_active according to user's status.

        Argument:
        status - user's status
        """
        if self.role == Role.objects.get(id=1):
            if not self.last_active_admin():
                self.is_active = (status == 0)
            else:
                self.is_active = True
                self.status = 0
        else:
            self.is_active = (status == 0)

    def set_is_staff(self, role):
        """Set is_staff according to user's role.

        Argument:
        Argument:
        role - user's role
        """
        self.is_staff = (role == Role.objects.get(id=1) or role == Role.objects.get(id=3))

    def get_short_name(self):
        """Return the user's email"""
        # The user is identified by the email address
        return self.email

    def get_full_name(self):
        """Return the user's name and email"""
        return self.name + " " + self.email

    def email_to_user(self, subject, message, sender=None, **kwargs):
        """Send an email to the user

        Arguments:
        subject - theme of the letter
        message - message of the email
        sender - sender/author of the email
        **kwargs - other arguments
        """
        send_mail(subject, message, sender, [self.email], **kwargs)

    def delete(self, *args, **kwargs):
        """Block the user instead of dropping.

        Put is_active into False and change status.
        Don't delete the last admin
        """
        if self.role == Role.objects.get(id=1):
            if not self.last_active_admin():
                self.is_active = False
                self.status = 1
                self.save()
        else:
            self.is_active = False
            self.status = 1
            self.save()

    def last_active_admin(self):
        """Return True if it is the last active admin."""
        number = User.objects.filter(role=1, is_active=True).count()
        if number > 1:
            return False
        else:
            return True

    def set_permissions(self, role):
        """Set user_permissions according to user's role.

        Argument:
        role - user's role
        """
        for perm in role.permissions.all():
            self.user_permissions.add(perm)