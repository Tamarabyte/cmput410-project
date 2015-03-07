from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login
from django.views.generic import TemplateView
from Hindlebook.forms import LoginForm
from django.contrib.auth.decorators import login_required
urlpatterns = patterns('',
    # Pre-login URLS
    url(r'^$', login, {'template_name' : 'login.html', 'authentication_form' : LoginForm}, name='login'),
    url(r'^stream$', login_required(TemplateView.as_view(template_name='placeholder.html')), name="stream"),
		url(r'^profile/(?P<authorID1>[0-9]+)/sendPost', 'Hindlebook.views.statusUpdate', name='statusUpdate'),
		url(r'^profile/(?P<authorID1>[0-9]+)', 'Hindlebook.views.profileQuery', name='profileQuery'),
    
    # Rest Api
    url(r'^api/', include('api.urls', namespace='api')),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Admin Site
    url(r'^admin/', include(admin.site.urls)),

)
