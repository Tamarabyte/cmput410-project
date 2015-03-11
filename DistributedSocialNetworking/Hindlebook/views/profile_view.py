from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.http import Http404
from django.views.generic import TemplateView, UpdateView, View
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from Hindlebook.models import Post, User
from Hindlebook.forms import ProfileEditForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from Hindlebook.forms import CommentForm
from django.core.exceptions import ValidationError

User = get_user_model()


class ProfileView(TemplateView):
    template_name = 'profile.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        authorUUID = self.kwargs.get('authorUUID', self.request.user.uuid)
        
        if (self.request.user.uuid == authorUUID):
            context['author_form'] = ProfileEditForm(instance=self.request.user)
            
        context['author'] = get_object_or_404(User, uuid=authorUUID)
        context['posts'] = Post.objects.filter(author__uuid=authorUUID)

        if self.request.user in list(context["author"].followed_by.all()):
            context['isFollowing'] = 1
        else:
            context['isFollowing'] = 0

        return context


class ProfileUpdateView(View):


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileUpdateView, self).dispatch(*args, **kwargs)

    def post(self, request, authorUUID, *args, **kwargs):
        template_name = 'edit_profile.html'
        form_name_in_template = "author_form"
        form_class = ProfileEditForm

        form = form_class(request.POST, request.FILES, instance=self.request.user)

        if not form.is_valid():
            response_data = {'form': render_to_string(template_name, {form_name_in_template : form})}
            return JsonResponse(response_data, status=400)

        obj = form.save(commit=True)
        return JsonResponse({}, status=200)


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
