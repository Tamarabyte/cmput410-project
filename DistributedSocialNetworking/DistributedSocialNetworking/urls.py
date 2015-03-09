from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login
from django.views.generic import TemplateView, RedirectView
from Hindlebook.forms import LoginForm
from Hindlebook.views import ProfileView, StreamView, RegistrationView, LogoutRedirect, PostView, CommentView, ProfileUpdateView
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Pre-login URLs
    url(r'^login/', login, {'template_name' : 'login.html', 'authentication_form' : LoginForm}, name='login'),
    url(r'^logout$', LogoutRedirect.as_view(), name='logout'),
    url(r'^register$', RegistrationView.as_view(), name='register'),

    # Stream URLs
    url(r'^$', StreamView.as_view(), name="stream"),

    # posting to posts
    url(r'^posts$', PostView.as_view(), name="posts"),
    url(r'^posts/(?P<postUUID>[\w-]+)', CommentView.as_view(), name="post_comments"),

    # Profile URLs
    url(r'^profile$', ProfileView.as_view(), name="personal_profile"),
    url(r'^author/(?P<pk>[\d]+)/edit', ProfileUpdateView.as_view(), name='edit_profile'),
    # url(r'^author/edit$', ProfileUpdateView.as_view(), name='edit_profile'),
    url(r'^profile/(?P<authorUUID>[\w-]+)', ProfileView.as_view(), name="profile"),

    # Search URLs
    url(r'^search$', 'Hindlebook.views.search', name="search"),

    # Rest Api
    url(r'^api/', include('api.urls', namespace='api')),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Admin Site
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
