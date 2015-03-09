from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse, QueryDict, HttpResponse
from django.core.exceptions import ValidationError

from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django import forms
from django.conf import settings


from Hindlebook.models.post_models import Post, Comment
from Hindlebook.models import user_models
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
        return context

class CreatePost(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreatePost, self).dispatch(*args, **kwargs)

    def put(self, request, postUUID, *args, **kwargs):
        put = QueryDict(request.body);
        form = PostForm(data=put)
        
        if not form.is_valid():
            response_data = { 'form' : render_to_string("post_form.html", {"post_form" : form}) }
            return JsonResponse(response_data, status=400)


        post = form.save(request.user ,postUUID, commit=False);
        try:
            post.full_clean()
        except ValidationError as e:
            errors = ""
            for value in e.message_dict.values():
                errors += ' '.join(value);
            response_data = { 'form' : render_to_string("post_form.html", {"post_form" : form, "alert" : errors }) }
            return JsonResponse(response_data, status=400)

        post.save()
        response_data = { 'form' : render_to_string("post_form.html", {"post_form" : PostForm()}) }
        response_data["post"] = render_to_string("post.html", {"post" : post, "MEDIA_URL" : settings.MEDIA_URL })
        return JsonResponse(response_data, status=201)

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        return context



