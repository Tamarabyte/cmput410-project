from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login
from django.views.generic import TemplateView
from Hindlebook.forms import LoginForm
from Hindlebook.views import ProfileView, StreamView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # Pre-login URLs
    url(r'^$', login, {'template_name' : 'login.html', 'authentication_form' : LoginForm}, name='login'),

    # Stream URLs
    url(r'^stream$', StreamView.as_view(), name="stream"),
		url(r'^profile/(?P<authorID1>[0-9]+)$', 'Hindlebook.views.profileQuery', name='profileQuery'),

    # Profile URLs
    url(r'^profile/(?P<authorID1>[0-9]+)', ProfileView.as_view()),

    # Search URLs
    url(r'^search$', 'Hindlebook.views.search', name="search"),

    # Rest Api
    url(r'^api/', include('api.urls', namespace='api')),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Admin Site
    url(r'^admin/', include(admin.site.urls)),

)
