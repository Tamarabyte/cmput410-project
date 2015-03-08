from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login
from django.views.generic import TemplateView
from Hindlebook.forms import LoginForm
from Hindlebook.views import ProfileView, StreamView, RegistrationView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # Pre-login URLs
    url(r'^$', login, {'template_name' : 'login.html', 'authentication_form' : LoginForm}, name='login'),
    url(r'^register$', RegistrationView.as_view(), name='register'),
    
    # Stream URLs
    url(r'^stream$', StreamView.as_view(), name="stream"),

    # Profile URLs
    url(r'^profile/(?P<authorID1>[0-9]+)', ProfileView.as_view()),

    # Search URLs
    url(r'^search/(?P<query>\w{0,50})/$', 'Hindlebook.views.search', name="search"),

    # Rest Api
    url(r'^api/', include('api.urls', namespace='api')),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Admin Site
    url(r'^admin/', include(admin.site.urls)),
)
