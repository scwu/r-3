from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from r3.views import hello
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
	url(r'^$', hello, {}, "R^3"),
    # Examples:
    # url(r'^$', 'r3.views.home', name='home'),
    # url(r'^r3/', include('r3.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
