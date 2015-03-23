from django.views.generic import ListView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
User = get_user_model()


class FriendsListView(ListView):
    template_name = 'friends.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        uuid = kwargs.get('uuid', self.request.user.uuid)
        self.author = get_object_or_404(User, uuid=self.uuid)
        return super(FriendsListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FriendsListView, self).get_context_data(**kwargs)
        context['follows'] = author.getFollowing()
        context['friends'] = author.getFriends()
        return context


