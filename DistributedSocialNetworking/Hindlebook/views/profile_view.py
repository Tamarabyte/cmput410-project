from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.views.generic import TemplateView, UpdateView
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from Hindlebook.models import Post, User
from Hindlebook.forms import ProfileEditForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from Hindlebook.forms import CommentForm

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
        if self.request.user in list(context["author"].followed_by.all()):
            context['isFollowing'] = 1
        else:
            context['isFollowing'] = 0
        print(get_object_or_404(User, uuid=authorUUID).uuid)
        print(self.request.user.uuid)
        return context


class ProfileUpdateView(UpdateView):
    template_name = 'edit_profile.html'
    model = User
    form_class = ProfileEditForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # uuid = kwargs.get('uuid', self.request.user.uuid)
        # self.user = get_object_or_404(User, uuid=self.uuid)
        return super(ProfileUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        # return HttpResponse(render_to_string('profile.html'))
        # return HttpResponse(render_to_string('profile.html', {'loan': loan}))
        return HttpResponseRedirect(reverse('personal_profile'))

    def get_context_data(self, **kwargs):
        # raise Http404("wtf3")
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        return context

class ProfileStreamView(TemplateView):
    template_name = "profile_stream.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileStreamView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileStreamView, self).get_context_data(**kwargs)
        authorUUID = self.kwargs.get('authorUUID', self.request.user.uuid)
        profile_user = User.objects.filter(uuid=authorUUID)
        context['posts'] = Post.objects_ext.get_profile_visibile_posts(active_user=self.request.user, page_user=profile_user )
        context['comment_form'] = CommentForm()
        return context
