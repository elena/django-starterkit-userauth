# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views import generic
from accounts.forms import ProfileForm, ProfileCreationForm
from accounts.models import Profile


class LoginRequiredMixin(object):

    required_permissions = None

    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        # Ensure the user has the required permissions. If the view should be
        # available to anyone, that must be explicitly set up by setting
        # required_permissions to an empty list.
        if self.required_permissions is None:
            raise ImproperlyConfigured(
                'This view has no permissions specified.')

        if request.user.has_perms(self.required_permissions):
            return super(LoginRequiredMixin, self).dispatch(
                request, *args, **kwargs)
        else:
            raise PermissionDenied


class QuerySetMixin(object):

    model = Profile

    def get_queryset(self, *args, **kwargs):
        queryset = super(QuerySetMixin, self).get_queryset(*args, **kwargs)
        return queryset.filter(is_active=True)


class EditMixin(QuerySetMixin):

    success_url = reverse_lazy("home")

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(EditMixin, self).get_form_kwargs(*args, **kwargs)
        return form_kwargs


class CreateView(EditMixin, SuccessMessageMixin, generic.CreateView):

    form_class = ProfileCreationForm
    required_permissions = ('accounts.add_user',)
    success_message = "User created."


class UpdateView(EditMixin, LoginRequiredMixin, SuccessMessageMixin,
                 generic.UpdateView):

    form_class = ProfileForm
    required_permissions = ('accounts.change_user',)
    success_message = "Profile updated."

    # Note that this is un unusual update view.
    # http://pydanny.com/django-update-view-without-slug-in-the-url.html
    def get_object(self):
        return self.request.user

