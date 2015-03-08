from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.template import RequestContext
from django import forms

from datetime import datetime

from Hindlebook.models.post_models import Post
from Hindlebook.models import user_models


class PostForm(forms.Form):
	text = forms.CharField()

	def make_post(self, user):
		new_p = Post(author=user, text=self.cleaned_data['text'] , pub_date=datetime.now())
		new_p.save()

class StreamView(FormView):
	template_name = "stream.html"
	form_class = PostForm
	success_url = "/stream"

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(StreamView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(StreamView, self).get_context_data(**kwargs)
		context['posts'] = Post.objects.all().order_by('-pub_date')
		return context

	def form_valid(self, form):
		form.make_post(self.request.user)
		return super(StreamView, self).form_valid(self)


