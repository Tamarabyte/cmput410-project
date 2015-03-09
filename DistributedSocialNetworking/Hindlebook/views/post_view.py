from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.template import RequestContext
from django.http import HttpResponse
from django import forms

from rest_framework.response import Response

from Hindlebook.models.post_models import Post
from Hindlebook.models import user_models
from Hindlebook.forms import PostForm
import Hindlebook


class PostView(View):

	@method_decorator(login_required)

	def dispatch(self, *args, **kwargs):
		return super(PostView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context['user'] = self.request.user
		return context

	def post(self, request):
		form = PostForm(request.POST, prefix="pos", request=request)

		response = HttpResponse()
		if (form.is_valid()):
			form.on_valid(self.request.user)
			response.status_code = 200
		else:
			response.status_code = 400

		return response