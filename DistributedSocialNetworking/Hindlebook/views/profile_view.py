from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404, JsonResponse
from django.views.generic import TemplateView, UpdateView
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

import dateutil
import datetime

from Hindlebook.models import Post, User, Comment
from Hindlebook.forms import ProfileEditForm, CommentForm

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

    def post(self, *args, **kwargs):
        authorUUID = self.kwargs.get('authorUUID', self.request.user.uuid)
        page_user = get_object_or_404(User, uuid=authorUUID)
        posts = []
        comments = []
        time = None
        if self.request.POST['last_time'] != '':
            time = dateutil.parser.parse(self.request.POST['last_time'])
        all_posts = Post.objects_ext.get_all_visibile_posts(active_user=self.request.user, page_user=page_user, reversed=False, min_time=time)
        for post in all_posts:
            response_data = {'form': render_to_string("post/post_form.html", {"post_form": PostForm()})}
            response_data["post"] = render_to_string("post/post.html", {"post": post, "MEDIA_URL": settings.MEDIA_URL})
            response_data["post"] += render_to_string("post/post_footer.html", {"post": post})
            response_data["created_guid"] = post.guid
            posts.append(response_data)

        if time is not None:
            all_comments = Comment.objects.filter(pubDate__gt=time, post__in=all_posts)
        else:
            all_comments = Comment.objects.filter(post__in=all_posts)

        for comment in all_comments:
            response_data = {'form': render_to_string("comment/comment_form.html", {"comment_form": PostForm()})}
            response_data["comment"] = render_to_string("comment/comment.html", {"comment": comment})
            response_data["postGUID"] = comment.post.guid
            comments.append(response_data)

        return JsonResponse({'posts': posts, 'comments': comments, 'time': datetime.datetime.now(dateutil.tz.tzutc()).isoformat()})


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
