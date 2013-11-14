#-*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from django.contrib.auth import forms as auth
from accounts.models import Profile


class AuthenticationForm(auth.AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.input_type = 'email'
        self.fields['username'].widget.attrs.update({'required': 'required',
            'autofocus': 'autofocus'})
        self.fields['password'].widget.attrs.update({'required': 'required'})


class ProfileChangeForm(forms.ModelForm):

    password = auth.ReadOnlyPasswordHashField()

    class Meta(object):
        model = Profile

    def __init__(self, *args, **kwargs):
        super(ProfileChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')


class ProfileCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput,
        help_text='Enter the same password as above, for verification.')

    class Meta(object):
        fields = ['email', 'casual_name', 'full_name']
        model = Profile

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The passwords don\'t match')
        return password2

    def save(self, commit=True):
        profile = super(ProfileCreationForm, self).save(commit=False)
        profile.set_password(self.cleaned_data['password1'])
        if commit:
            profile.save()
        return profile


class ProfileForm(forms.ModelForm):

    class Meta(object):
        fields = ['email', 'casual_name', 'full_name', 'is_active']
        model = Profile

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'required': 'required'})
        self.fields['email'].widget.input_type = 'email'



