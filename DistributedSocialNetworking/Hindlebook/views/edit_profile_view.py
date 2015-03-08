from django.shortcuts import render, render_to_response,redirect
from django.template import Template, RequestContext
from django.http import HttpResponse, JsonResponse, HttpRequest, Http404
from django.views.generic.edit import UpdateView
from Hindlebook.models import Post, User
from Hindlebook.forms import PostForm
import json


