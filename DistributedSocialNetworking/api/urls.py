from django.conf.urls import patterns, url

urlpatterns = patterns('',

    # URL for GET requests to check if two authors are friends
    url(r'^friends/(?P<authorID1>[0-9]+)/(?P<authorID2>[0-9]+)$', 'api.views.friend2friendQuery', name='friend2friendQuery'),

    # URL for POST requests to check if the author ID in URL is friends with any in the given JSON list
    url(r'^friends/(?P<authorID1>[0-9]+)$', 'api.views.friendQuery', name='friendQuery'),

    # URL for POST friend requests
    url(r'^friendrequest$', 'api.views.friendRequest', name='friendRequest'),
)
