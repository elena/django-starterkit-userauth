# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, patterns, url
from accounts.views import profile

urls = patterns('accounts.views',

    # Login/Logout
    url(r'^login$', 'login', name='login'),
    url(r'^logout$', 'logout', name='logout'),

    # # Create/Edit Profile
    url(r'^register$', profile.CreateView.as_view(), name='profile_create'),
    url(r'^edit$', profile.UpdateView.as_view(), name='profile_edit'),

    # Password
    ### Change
    url(r'^password/change/$', 'password_change', name='password_change'),
    url(r'^password/change/complete$', 'password_change_done',
        name='password_change_done'),

    ### Reset
    url(r'^password/reset/$', 'password_reset', name='password_reset'),
    url(r'^password/reset/sent$', 'password_reset_done',
       name='password_reset_done'),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]'
       '{1,13}-[0-9A-Za-z]{1,20})/$', 'password_reset_confirm',
       name='password_reset_confirm'),
    url(r'^password/reset/complete$', 'password_reset_complete',
       name='password_reset_complete'),
)

urlpatterns = patterns('',
    (r'^', include(urls, namespace='accounts')),
)
