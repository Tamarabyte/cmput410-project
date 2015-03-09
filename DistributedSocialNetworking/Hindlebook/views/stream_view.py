from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse, QueryDict
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.conf import settings


from Hindlebook.models.post_models import Post, Comment
from Hindlebook.forms import PostForm, CommentForm


class StreamView(TemplateView):
    template_name = "stream.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StreamView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StreamView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-pub_date')
        context['post_form'] = PostForm()
        context['comment_form'] = CommentForm()
        return context

class CreatePost(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreatePost, self).dispatch(*args, **kwargs)

    def put(self, request, postUUID, *args, **kwargs):
        put = QueryDict(request.body);
        form = PostForm(data=put)
        
        if not form.is_valid():
            response_data = { 'form' : render_to_string( "post/post_form.html", {"post_form" : form}) }
            return JsonResponse(response_data, status=400)


        post = form.save(request.user ,postUUID, commit=False);
        try:
            post.full_clean()
        except ValidationError as e:
            errors = ""
            for value in e.message_dict.values():
                errors += ' '.join(value);
            response_data = { 'form' : render_to_string("post/post_form.html", {"post_form" : form, "alert" : errors }) }
            return JsonResponse(response_data, status=400)

        post.save()
        response_data = { 'form' : render_to_string( "post/post_form.html", {"post_form" : PostForm()}) }

        response_data["post"] = render_to_string("post/post.html", {"post" : post, "MEDIA_URL" : settings.MEDIA_URL })
        response_data["post"] += render_to_string("post/post_footer.html", {"post" : post})
        response_data["created_uuid"] = post.uuid;
        return JsonResponse(response_data, status=201)


class CreateComment(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateComment, self).dispatch(*args, **kwargs)

    def put(self, request, postUUID, commentUUID, *args, **kwargs):
        put = QueryDict(request.body);
        form = CommentForm(data=put)

        if not form.is_valid():
            response_data = { 'form' : render_to_string("comment/comment_form.html", {"comment_form" : form}), 'errors': form.errors }
            return JsonResponse(response_data, status=400)

        post = get_object_or_404(Post, uuid=postUUID)
        comment = form.save(request.user, post, commentUUID, commit=False);

        try:
            comment.full_clean()
        except ValidationError as e:
            errors = ""
            for value in e.message_dict.values():
                errors += ' '.join(value);
            response_data = { 'form' : render_to_string("comment/comment_form.html", {"comment_form" : form, "alert" : errors }) }
            return JsonResponse(response_data, status=400)

        comment.save()
        response_data = { 'form' : render_to_string("comment/comment_form.html", {"comment_form" : PostForm()}) }
        response_data["comment"] = render_to_string("comment/comment.html", {"comment" : comment })
        return JsonResponse(response_data, status=201)



