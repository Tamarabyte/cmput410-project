from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext

from Hindlebook.models.post_models import Post
from Hindlebook.models import user_models

def stream(request):
	context = RequestContext(request)
	posts = Post.objects.all().order_by('-pub_date')
	return render_to_response('stream.html', {"posts":posts}, context)