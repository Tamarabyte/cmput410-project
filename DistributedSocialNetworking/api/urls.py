from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    # GET, POST, PUT for posts by ID
    url(r'^post/(?P<postID>[-\w]+)$', views.PostDetail.as_view(), name='postByID'),

    # GET for friend2friend querying
    url(r'^friends/(?P<authorID1>[-\w]+)/(?P<authorID2>[-\w]+)$', views.Friend2Friend.as_view(), name='friend2friend'),

    # POST for friend querying
    url(r'^friends/(?P<authorID1>[-\w]+)$', views.FriendQuery.as_view(), name='friendQuery'),

    # POST for friend requesting
    url(r'^friendrequest$', views.FriendRequest.as_view(), name='friendRequest'),

    # GET for author posts by ID
    url(r'^author/(?P<authorID>[-\w]+)/posts$', views.AuthorPosts.as_view(), name='authorPosts'),

    # GET all public posts
    url(r'^posts$', views.PublicPosts.as_view(), name='publicPosts'),
]

urlpatterns = format_suffix_patterns(urlpatterns) 
