from django import forms

from datetime import datetime

from Hindlebook.models.post_models import Post
from Hindlebook.forms.template_mixin import TemplateMixin


class PostForm(forms.Form, TemplateMixin):
	text = forms.CharField()

	def form_valid(self, user):
		new_p = Post(author=user, text=self.cleaned_data['text'] , pub_date=datetime.now())
		new_p.save()
