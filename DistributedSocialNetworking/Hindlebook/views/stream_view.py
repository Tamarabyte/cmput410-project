from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext

from Hindlebook.models.post_models import Post
from Hindlebook.models import user_models

class StreamView(TemplateView):

	template_name = "stream.html"

	def get_context_data(self, **kwargs):
		context = super(StreamView, self).get_context_data(**kwargs)
		context['posts'] = Post.objects.all().order_by('-pub_date')
		return context