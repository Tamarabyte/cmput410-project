from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Temporary crap home page
    url(r'^$', 'Hindlebook.views.home', name='home'),

    # Rest Api
    url(r'^api/', include('api.urls', namespace='api')),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', include(admin.site.urls)),
)
