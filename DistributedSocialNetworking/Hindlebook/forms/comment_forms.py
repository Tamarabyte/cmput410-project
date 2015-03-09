import uuid
from django import forms
from django.core.exceptions import ValidationError

from datetime import datetime

from Hindlebook.models.post_models import Post, Comment
from Hindlebook.forms.template_mixin import TemplateMixin



class CommentForm(forms.Form, TemplateMixin):
	text = forms.CharField()
	post_UUID = None

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		self.post_UUID = kwargs.pop('post_UUID', None)
		super(CommentForm, self).__init__(*args, **kwargs)

	def set_postUUID(self, post_uuid):
			self.post_UUID = post_UUID

	def on_valid(self, user):
		p = Post.objects.get(uuid=self.cleaned_data['post_uuid'])
		if p != None:
			new_f = Comment(author=user, text=self.cleaned_data['text'], pub_date=datetime.now(), post=p)
			new_f.save()
			
	def clean(self):
		cleaned_data = self.cleaned_data
		post_id_key = 'post_uuid'
		if self.post_UUID != None:
			post = str(uuid.UUID(self.post_UUID))
			cleaned_data[post_id_key] = post
		else:
			raise ValidationError("%s key is not in form" %(post_id_key))

		return cleaned_data

