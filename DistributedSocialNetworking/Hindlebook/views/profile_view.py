from django.http import Http404
from Hindlebook.models import Post, User
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
User = get_user_model()

class ProfileView(TemplateView):
    template_name = 'profile.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        
        authorUUID = self.kwargs.get('authorUUID', self.request.user.uuid)
        context['author'] = get_object_or_404(User, uuid=authorUUID)
        context['posts'] = Post.objects.filter(author__uuid=authorUUID)
        
        return context
