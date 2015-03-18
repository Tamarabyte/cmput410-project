from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from api.views import PublicPosts, PostDetails, AuthoredPosts, VisiblePosts
from api.routers import CustomSimpleRouter

urlpatterns = [
    # GET, POST, PUT for posts by ID
    # url(r'^post/(?P<postID>[-\w]+)$', views.PostDetail.as_view(), name='postByID'),
    url(r'^post/(?P<guid>[-\w]+)$', PostDetails.as_view(), name='postByID'),

    # GET for friend2friend querying
    url(r'^friends/(?P<authorID1>[-\w]+)/(?P<authorID2>[-\w]+)$', views.Friend2Friend.as_view(), name='friend2friend'),

    # POST for friend querying
    url(r'^friends/(?P<authorID1>[-\w]+)$', views.FriendQuery.as_view(), name='friendQuery'),

    # POST for friend requesting
    url(r'^friendrequest$', views.FriendRequest.as_view(), name='friendRequest'),

    # POST for unfriending
    url(r'^unfriend$', views.UnfriendRequest.as_view(), name='unfriendRequest'),

    # POST for following
    url(r'^follow$', views.FollowRequest.as_view(), name='followRequest'),

    # POST for unfollowing
    url(r'^unfollow$', views.UnfollowRequest.as_view(), name='unfollowRequest'),

    # GET for author posts by ID
    # http://service/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
    url(r'^author/(?P<uuid>[-\w]+)/posts$', AuthoredPosts.as_view(), name='authoredPosts'),

    # GET all public posts
    # http://service/posts (all posts marked as public on the server)
    url(r'^posts$', PublicPosts.as_view(), name='publicPosts'),

    # GET visible posts
    # http://service/author/posts (posts that are visible to the currently authenticated user)
    url(r'^author/posts$', VisiblePosts.as_view(), name='visiblePosts'),
]

router = CustomSimpleRouter()
router.register('author', views.AuthorViewSet, base_name="User")
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)

