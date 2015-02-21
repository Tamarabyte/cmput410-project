from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Temporary crap home page
    url(r'^$', 'Hindlebook.views.home', name='home'),

    # URL for GET requests to check if two authors are friends
    url(r'^friends/(?P<authorID1>[0-9]+)/(?P<authorID2>[0-9]+)', 'Hindlebook.views.friend2friendQuery', name='friend2friendQuery'),
    
    # URL for POST requests to check if the author ID in URL is friends with any in the given JSON list
    url(r'^friends/(?P<authorID1>[0-9]+)', 'Hindlebook.views.friendQuery', name='friendQuery'),

    url(r'^admin/', include(admin.site.urls)),
)
