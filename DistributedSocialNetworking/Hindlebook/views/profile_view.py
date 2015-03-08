from django.http import Http404
from Hindlebook.models import Post, User
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class ProfileView(TemplateView):
    template_name = 'profile.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        profileID = self.kwargs['profileID']
        try:
            profile = User.objects.get(id=profileID)
        except User.DoesNotExist:
            raise Http404("User does not exist")

        context['author'] = User.objects.filter(id=profileID).first()
        context['posts'] = Post.objects.filter(author_id=profileID)

        context['notification_count'] = getFriendRequestCount()
        return context
