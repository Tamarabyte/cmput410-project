from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from Hindlebook.models import Author


class FriendsView(TemplateView):
    template_name = 'friends/friends.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        uuid = kwargs.get('authorUUID', self.request.user.author.uuid)
        self.author = get_object_or_404(Author, uuid=uuid)
        return super(FriendsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FriendsView, self).get_context_data(**kwargs)
        context['author'] = self.author
        return context
