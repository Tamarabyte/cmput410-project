from django.shortcuts import render, render_to_response,redirect
from django.template import Template, RequestContext
from django.http import HttpResponse, JsonResponse, HttpRequest, Http404
from Hindlebook.models import Post, User
from Hindlebook.forms import PostForm
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import json

class ProfileView(TemplateView):
    template_name = 'profile.html'
    posts = []
    user = -1
    fname = ""
    lname = ""
    author = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        authorID1 = self.kwargs['authorID1']
        username = None
        if self.request.user.is_authenticated():
            username = self.request.user.username
        try:
	        profile = User.objects.get(id=authorID1)
        except User.DoesNotExist:
	        raise Http404("User does not exist")
        posts = Post.objects.filter(author_id=authorID1)
        user = User.objects.filter(id=authorID1).first()
        context['posts'] = posts
        context['user'] = self.request.user
        context['fname'] = user.first_name
        context['lname'] = user.last_name
        context['author'] = user
        # Set this to the number of pending friend reuqests ltaer
        context['notification_count'] = 0
        return context

    def get_template_names(self):
        authorID1 = self.kwargs['authorID1']

        if self.request.user.is_authenticated():
            username = self.request.user.username
        try:
	        profile = User.objects.get(id=authorID1)
        except User.DoesNotExist:
	        raise Http404("User does not exist")
        user = User.objects.filter(id=authorID1).first()
            
        if (username == user.username):
            self.template_name = "selfProfile.html"
        return [self.template_name]

"""
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
"""
"""
def profileQuery(request, authorID1):

	if (request.method != "GET"):
		raise Http404("Should be a GET request")
	

	try:
		profile = User.objects.get(id=authorID1)
	except User.DoesNotExist:
		raise Http404("User does not exist")

	context = RequestContext(request)
	form = PostForm()
	posts = Post.objects.filter(author_id=authorID1)
	user = User.objects.filter(id=authorID1).first()
	
	if (request.method == 'POST'):
		posttext = request.POST.get("post_text","")
		newpost = Post(author_id = authorID1, text=posttext)
		newpost.save()

	return render_to_response("profile.html",{'posts':posts,'form':form,'author':authorID1,'fname':user.first_name,'lname':user.last_name},context)
	
def statusUpdate(request, authorID1):

	if (request.method != "POST"):
		raise Http404("Should be a POST")
	
	posttext = request.POST.get("post_text","")
	newpost = Post(author_id = authorID1, text=posttext,privacy=request.POST.get("post_privacy"))
	newpost.save()
	context = RequestContext(request)

	return redirect("/profile/"+authorID1)
"""


