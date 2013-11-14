# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib import messages
from django.contrib.auth import views as auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from accounts.forms import AuthenticationForm


## Extending functions from django.contribut.auth (as auth.*)

def login(request, *args, **kwargs):
    defaults = {
        'authentication_form': AuthenticationForm,
        'template_name': 'accounts/login.html',
    }
    for key, value in defaults.items():
        kwargs.setdefault(key, value)
    return auth.login(request, *args, **kwargs)


def logout(request, *args, **kwargs):
    defaults = {
        'template_name': 'accounts/logged_out.html',
    }
    for key, value in defaults.items():
        kwargs.setdefault(key, value)
    return auth.logout(request, *args, **kwargs)


@login_required
def password_change(request, *args, **kwargs):
    defaults = {
        'template_name': 'accounts/password_change_form.html',
        'post_change_redirect': reverse('accounts:password_change_done'),
    }
    for key, value in defaults.items():
        kwargs.setdefault(key, value)
    return auth.password_change(request, *args, **kwargs)


@login_required
def password_change_done(request, *args, **kwargs):
    messages.success(request, 'Your password has been changed.')
    return redirect('home')


def password_reset(request, *args, **kwargs):
    defaults = {
        'template_name': 'accounts/password_reset_form.html',
        'email_template_name': 'accounts/password_reset_email.txt',
        'post_reset_redirect': reverse('accounts:password_reset_done'),
    }
    for key, value in defaults.items():
        kwargs.setdefault(key, value)
    return auth.password_reset(request, *args, **kwargs)


def password_reset_done(request, *args, **kwargs):
    defaults = {
        'template_name': 'accounts/password_reset_done.html',
    }
    for key, value in defaults.items():
        kwargs.setdefault(key, value)
    return auth.password_reset_done(request, *args, **kwargs)


def password_reset_confirm(request, *args, **kwargs):
    defaults = {
        'template_name': 'accounts/password_reset_confirm.html',
        'post_reset_redirect': reverse('accounts:password_reset_complete'),
    }
    for key, value in defaults.items():
        kwargs.setdefault(key, value)
    return auth.password_reset_confirm(request, *args, **kwargs)


def password_reset_complete(request, *args, **kwargs):
    defaults = {
        'template_name': 'accounts/password_reset_complete.html',
    }
    for key, value in defaults.items():
        kwargs.setdefault(key, value)
    return auth.password_reset_complete(request, *args, **kwargs)


