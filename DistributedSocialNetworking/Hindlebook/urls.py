from django.conf.urls import patterns, url

urlpatterns = patterns('',
	#  URL for viewing a user profile.
		url(r'^(?P<authorID1>[0-9]+)/', 'Hindlebook.views.profileQuery', name='profileQuery'),
)
