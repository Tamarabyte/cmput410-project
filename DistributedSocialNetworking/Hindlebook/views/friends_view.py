from django.views.generic import ListView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from Hindlebook.models import Author


class FriendsListView(ListView):
    template_name = 'friends.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        uuid = kwargs.get('uuid', self.request.user.author.uuid)
        self.author = get_object_or_404(Author, uuid=uuid)
        return super(FriendsListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FriendsListView, self).get_context_data(**kwargs)
        context['follows'] = self.author.getFollowing()
        context['friends'] = self.author.getFriends()
        return context
