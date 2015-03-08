from django.http import Http404
from django.views.generic import TemplateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from Hindlebook.models import Post, User
from Hindlebook.forms import EditProfileForm


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


class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'profile_form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponse(render_to_string('profile_edit_form_success.html'))
