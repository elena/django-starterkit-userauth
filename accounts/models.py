# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from accounts.managers import ProfileManager


class Profile(AbstractBaseUser, PermissionsMixin):
    """Customised user model.
    """

    email = models.EmailField('email address', max_length=254, unique=True)
    """ Email to be used as username. """

    casual_name = models.CharField(max_length=254, blank=True, default='')
    """ Name used for casual and often reference.

    Example: "Hi there [casual_name]!"
    """

    full_name = models.CharField(max_length=254, blank=True, default='')
    """ Full and complete formal name. """

    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff', default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False,
                                      blank=True, null=True)
    """:py:class:`datetime` for when this object was first created."""

    updated_at = models.DateTimeField(auto_now=True, editable=False,
                                      blank=True, null=True)
    """:py:class:`datetime` for when this object was last updated."""

    objects = ProfileManager()

    USERNAME_FIELD = 'email'

    class Meta(AbstractBaseUser.Meta):
        ordering = ('email',)
        permissions = (('read_user', 'Can read user'),)
        get_latest_by = 'created_at'

    def save(self, user=None, **kwargs):
        if user is not None:
            if not self.pk:
                self.created_by = user
            self.updated_by = user
        return super(Profile, self).save(**kwargs)

    def email_user(self, subject, message, from_email=None):
        """ Sends an email to this User.
        """

        send_mail(subject, message, from_email, [self.email])
