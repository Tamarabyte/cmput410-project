from django import forms

from datetime import datetime

from Hindlebook.models.post_models import Post, Comment
from Hindlebook.forms.template_mixin import TemplateMixin



class CommentForm(forms.Form, TemplateMixin):
	text = forms.CharField()

	def form_valid(self, user, post_id=None):
		p = Post.objects.get(id=post_id)
		if p != None:
			new_f = Comment(author=user, text=self.cleaned_data['text'], pub_date=datetime.now(), post=p)
			new_f.save()
