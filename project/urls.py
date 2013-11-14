from django.conf.urls import patterns, include, url
from .views import HomePageView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', HomePageView.as_view(), name='home'),

    ## User login.
    url(r'^user/', include('accounts.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

