from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse, QueryDict
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.conf import settings

import datetime
import dateutil.parser

from Hindlebook.models import Post, Comment
from Hindlebook.forms import PostForm, CommentForm
from api.json_derulo import getForeignStreamPosts

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
        return context

    def post(self, *args, **kwargs):
        posts = []
        comments = []
        time = None
        if self.request.POST['last_time'] != '':
            time = dateutil.parser.parse(self.request.POST['last_time'])
        new_posts = Post.objects_ext.get_all_visibile_posts(active_author=self.request.user.author, reversed=False, min_time=time) + getForeignStreamPosts(self.request.user.author,time)
        new_posts.sort(key=lambda p: p.pubDate)
        for post in new_posts:
            response_data = {'form': render_to_string("post/post_form.html", {"post_form": PostForm()})}
            response_data["post"] = render_to_string("post/post.html", {"post": post, "MEDIA_URL": settings.MEDIA_URL})
            response_data["post"] += render_to_string("post/post_footer.html", {"post": post})
            response_data["created_guid"] = post.guid
            posts.append(response_data)

        if time is not None:
            all_comments = Comment.objects.filter(pubDate__gt=time)
        else:
            all_comments = Comment.objects.all()

        for comment in all_comments:
            response_data = {'form': render_to_string("comment/comment_form.html", {"comment_form": PostForm()})}
            response_data["comment"] = render_to_string("comment/comment.html", {"comment": comment})
            response_data["postGUID"] = comment.post.guid
            comments.append(response_data)

        return JsonResponse({'posts': posts, 'comments': comments, 'time': datetime.datetime.now(dateutil.tz.tzutc()).isoformat()})


class CreatePost(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreatePost, self).dispatch(*args, **kwargs)

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
        response_data = {'form': render_to_string("post/post_form.html", {"post_form": PostForm()})}
        response_data["time"] = datetime.datetime.now(dateutil.tz.tzutc()).isoformat()
        response_data["post"] = render_to_string("post/post.html", {"post": post, "MEDIA_URL": settings.MEDIA_URL})
        response_data["post"] += render_to_string("post/post_footer.html", {"post": post})
        response_data["created_guid"] = post.guid
        return JsonResponse(response_data, status=201)


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

        response_data = {'form': render_to_string("comment/comment_form.html", {"comment_form": CommentForm()})}
        response_data["comment"] = render_to_string("comment/comment.html", {"comment": comment})
        response_data["time"] = datetime.datetime.now(dateutil.tz.tzutc()).isoformat()
        return JsonResponse(response_data, status=201)
