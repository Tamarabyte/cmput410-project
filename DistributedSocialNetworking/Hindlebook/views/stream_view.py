from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse, QueryDict
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse

import datetime
import dateutil.parser

from itertools import chain

from Hindlebook.models import Post, Comment
from Hindlebook.forms import PostForm, CommentForm
from api import json_derulo
from api.serializers import CommentSerializer


class StreamView(TemplateView):

    template_name = "stream.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StreamView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StreamView, self).get_context_data(**kwargs)
        context['posts'] = None
        context['post_form'] = PostForm()
        context['comment_form'] = CommentForm()
        context['github_id'] = self.request.user.author.github_id
        return context

    def post(self, *args, **kwargs):
        posts = []
        comments = []
        o_time = datetime.datetime.now(dateutil.tz.tzutc()).isoformat()
        time = None
        if self.request.POST['last_time'] != '':
            time = dateutil.parser.parse(self.request.POST['last_time'])
            # time = time + datetime.timedelta(0, 3)
            json_derulo.getForeignStreamPosts(self.request.user.author, time)
        local_posts = Post.objects.get_all_visibile_posts(active_author=self.request.user.author, reversed=False, min_time=time)
        user_id = self.request.user.author.uuid
        for post in local_posts:
            response_data = {}
            response_data["post"] = render_to_string("post/post.html", {"post": post, "user_id": user_id, "MEDIA_URL": settings.MEDIA_URL})
            response_data["post"] += render_to_string("post/post_footer.html", {"post": post})
            response_data["created_guid"] = post.guid
            posts.append(response_data)

        if time is not None:
            all_comments = Comment.objects.filter(pubDate__gt=time)
        else:
            all_comments = Comment.objects.all()

        for comment in all_comments:
            response_data = {}
            response_data["comment"] = render_to_string("comment/comment.html", {"comment": comment})
            response_data["postGUID"] = comment.post.guid
            comments.append(response_data)

        return JsonResponse({'posts': posts, 'comments': comments, 'time': o_time})


class PostView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PostView, self).dispatch(*args, **kwargs)

    def put(self, request, postGUID, *args, **kwargs):
        put = QueryDict(request.body)
        form = PostForm(data=put)

        if not form.is_valid():
            response_data = {'form': render_to_string("post/post_form.html", {"post_form": form})}
            return JsonResponse(response_data, status=400)

        post = form.save(request.user.author, postGUID, commit=False)

        # Validate all remaining fields not included in the post form, based on model constraints
        try:
            post.full_clean()
        except ValidationError as e:
            errors = ""
            for value in e.message_dict.values():
                errors += ' '.join(value)
            response_data = {'form': render_to_string("post/post_form.html", {"post_form": form, "alert": errors})}
            return JsonResponse(response_data, status=400)

        post.save()
        # When we don't pass form.save(commit=True) we have to explicitly save m2m fields later
        form.save_m2m()
        user_id = request.user.author.uuid
        response_data = {'form': render_to_string("post/post_form.html", {"post_form": PostForm()})}
        response_data["time"] = datetime.datetime.now(dateutil.tz.tzutc()).isoformat()
        response_data["post"] = render_to_string("post/post.html", {"post": post, "user_id": user_id, "MEDIA_URL": settings.MEDIA_URL})
        response_data["post"] += render_to_string("post/post_footer.html", {"post": post})
        response_data["created_guid"] = post.guid
        return JsonResponse(response_data, status=201)

    def delete(self, request, postGUID, *args, **kwargs):
        print(postGUID)
        post = Post.objects.get(guid=postGUID)
        if (request.user.author.uuid == post.author.uuid):
            post.is_deleted = True
            post.save()
        return JsonResponse({}, status=200)


class CreateComment(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateComment, self).dispatch(*args, **kwargs)

    def put(self, request, postGUID, commentGUID, *args, **kwargs):
        put = QueryDict(request.body)
        form = CommentForm(data=put)

        if not form.is_valid():
            response_data = {'form': render_to_string("comment/comment_form.html", {"comment_form": form}), 'errors': form.errors}
            return JsonResponse(response_data, status=400)

        post = get_object_or_404(Post, guid=postGUID)
        comment = form.save(request.user.author, post, commentGUID, commit=False)

        # Validate all remaining fields not included in the comment form, based on model constraints
        try:
            comment.full_clean()
        except ValidationError as e:
            errors = ""
            for value in e.message_dict.values():
                errors += ' '.join(value)
            response_data = {'form': render_to_string("comment/comment_form.html", {"comment_form": form, "alert": errors})}
            return JsonResponse(response_data, status=400)

        comment.save()
        try:
            if post.isForeign():
                print("Is foreign")
                json_derulo.sendForeignComment(comment, post.author.node)
        except Exception as e:
            print(str(e))

        response_data = {'form': render_to_string("comment/comment_form.html", {"comment_form": CommentForm()})}
        response_data["comment"] = render_to_string("comment/comment.html", {"comment": comment})
        response_data["time"] = datetime.datetime.now(dateutil.tz.tzutc()).isoformat()
        return JsonResponse(response_data, status=201)
