import uuid
from django import forms

from datetime import datetime

from Hindlebook.models.post_models import Post, Comment
from Hindlebook.forms.template_mixin import TemplateMixin



class CommentForm(forms.Form, TemplateMixin):
	text = forms.CharField()

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(CommentForm, self).__init__(*args, **kwargs)

	def on_valid(self, user):
		post = uuid.UUID(self.data['post_id'])
		print(post)
		if (post != None):
			p = Post.objects.get(id=post)
			if p != None:
				new_f = Comment(author=user, text=self.cleaned_data['text'], pub_date=datetime.now(), post=p)
				new_f.save()
