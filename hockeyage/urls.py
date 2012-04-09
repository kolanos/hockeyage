from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login', 'django.contrib.auth.views.login'),
    url(r'^logout', 'django.contrib.auth.views.logout'),
    #url(r'^logout', 'django.contrib.auth.views.logout_then_login'),
    url(r'^password_change', 'django.contrib.auth.views.password_change'),
    url(r'^password_change_done',
        'django.contrib.auth.views.password_change_done'),
    url(r'^password_reset', 'django.contrib.auth.views.password_reset'),
    url(r'^password_reset_done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^password_reset_confirm',
        'django.contrib.auth.views.password_reset_confirm'),
    url(r'^password_reset_complete',
        'django.contrib.auth.views.password_reset_complete'),
)
