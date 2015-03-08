from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django import forms

from Hindlebook.models.post_models import Post, Comment
from Hindlebook.models import user_models
from Hindlebook.forms import PostForm, CommentForm


class StreamView(TemplateView):
	template_name = "stream.html"
	post_form = PostForm(prefix="pos")
	comment_form = CommentForm(prefix="com")
	success_url = "stream"

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(StreamView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(StreamView, self).get_context_data(**kwargs)
		context['posts'] = Post.objects.all().order_by('-pub_date')
		context['user'] = self.request.user
		context['post_form'] = self.post_form
		context['comment_form'] = self.comment_form
		return context




