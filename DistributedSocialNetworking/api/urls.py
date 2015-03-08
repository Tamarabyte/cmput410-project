from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'^post/(?P<postID>[-\w]+)$', views.PostDetail.as_view(), name='postByID'),
    url(r'^friends/(?P<authorID1>[-\w]+)/(?P<authorID2>[-\w]+)$', views.Friend2Friend.as_view(), name='friend2friend'),
    url(r'^friends/(?P<authorID1>[-\w]+)$', views.FriendQuery.as_view(), name='friendQuery'),
    url(r'^friendrequest$', views.FriendRequest.as_view(), name='friendRequest'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
