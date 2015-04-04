from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login
from Hindlebook.forms import LoginForm
from Hindlebook.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = patterns('',

    # Admin Site
    url(r'^admin/', include(admin.site.urls)),

    # Pre-login URLs
    url(r'^login/', login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout$', LogoutRedirect.as_view(), name='logout'),
    url(r'^register$', RegistrationView.as_view(), name='register'),

    # Stream URLs
    url(r'^$', StreamView.as_view(), name="stream"),
    url(r'^myStream', FollowingStreamView.as_view(), name="following_stream"),
    url(r'^author/posts', RedirectView.as_view(pattern_name='stream')),
    url(r'^post/create/(?P<postGUID>[\w-]+)', PostView.as_view(), name="create_post"),
    url(r'^post/(?P<postGUID>[\w-]+)/create/(?P<commentGUID>[\w-]+)', CreateComment.as_view(), name="create_post"),
    url(r'^post/(?P<postGUID>[\w-]+)', PostView.as_view(), name="delete_post"),

    # Profile URLs
    url(r'^profile/(?P<authorUUID>[\w-]+)/edit', ProfileUpdateView.as_view(), name='edit_profile'),
    url(r'^profile/(?P<authorUUID>[\w-]+)$', ProfileView.as_view(), name="profile"),
    url(r'^author/(?P<authorUUID>[\w-]+)/posts', ProfileStreamView.as_view(), name="profile_stream"),

    # Friends URLs
    url(r'^requests$', NotificationsView.as_view(), name='requests'),
    url(r'^friends$', FriendsView.as_view(), name='friends'),
    url(r'^friends/(?P<authorUUID>[\w-]+)', FriendsView.as_view(), name='friends_view'),

    # Rest Api
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
