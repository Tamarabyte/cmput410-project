from django.shortcuts import render, render_to_response, redirect
from django.template import Template, RequestContext
from django.http import HttpResponse, JsonResponse, HttpRequest, Http404
from Hindlebook.models import Post, User
from Hindlebook.forms import PostForm
import json


def myProfile(request):
    pass


def profileQuery(request, authorID1):
    """ Handles requesting a user profile """
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
        posttext = request.POST.get("post_text", "")
        newpost = Post(author_id=authorID1, text=posttext)
        newpost.save()

    return render_to_response("profile.html", {'posts': posts, 'form': form, 'author': authorID1, 'fname': user.first_name, 'lname': user.last_name}, context)


def statusUpdate(request, authorID1):
    """ Handles status update posts"""
    if (request.method != "POST"):
        raise Http404("Should be a POST")

    posttext = request.POST.get("post_text", "")
    newpost = Post(author_id=authorID1, text=posttext)
    newpost.save()
    context = RequestContext(request)

    return redirect("/profile/" + authorID1)
