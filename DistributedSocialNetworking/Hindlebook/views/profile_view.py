from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404, JsonResponse, QueryDict
from django.views.generic import TemplateView, UpdateView, View
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

import dateutil
import datetime
import json


from Hindlebook.models import Post, Author, Comment
from Hindlebook.forms import ProfileEditForm, CommentForm
from api.json_derulo import getForeignAuthor, getForeignAuthorPosts





class ProfileView(TemplateView):
    template_name = 'profile.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        authorUUID = self.kwargs.get('authorUUID', self.request.user.author.uuid)
        profile_author = Author.objects.filter(uuid=authorUUID)
        context['comment_form'] = CommentForm()

        # get the profile edit form if our requesting user is viewing their own profile
        if (self.request.user.author.uuid == authorUUID):
            context['author_form'] = ProfileEditForm(instance=self.request.user.author)

        # get the author from the authorUUID in the URL
        context['author'] = Author.objects.filter(uuid=authorUUID).first()
        if context['author'] is None:
            local = False
        else:
            local = not context['author'].isForeign()

        if local:
            context['posts'] = Post.objects_ext.get_profile_visibile_posts(active_author=self.request.user.author, page_author=profile_author )

            if self.request.user.author in list(context["author"].followed_by.all()):
                context['isFollowing'] = 1
            else:
                context['isFollowing'] = 0
            if self.request.user.author in list(context["author"].friends_of.all()):
                context['isFriends'] = 1
            else:
                context['isFriends'] = 0
        else:
            # Have to change from JSON to object because Mark wants JSON and Ajax
            author = getForeignAuthor(authorUUID)
            if author:
                # If we found the author we should set the other vars as
                # necessary, if not we should 404
                # Currently not setting up crap cuz i'm waiting for changes from m+t
                context['author'] = author
                context['isFollowing'] = 0
                context['isFriends'] = 0
                postsJSON = getForeignAuthorPosts(authorUUID)
                if postsJSON:
                    postsObj = json.loads(postsJSON)
                    context['posts'] = postsObj
            else:
                raise Http404("No Author matches the given query.")

        return context

    def post(self, *args, **kwargs):
        authorUUID = self.kwargs.get('authorUUID', self.request.user.author.uuid)
        page_author = get_object_or_404(Author, uuid=authorUUID)
        posts = []
        comments = []
        time = None
        if self.request.POST['last_time'] != '':
            time = dateutil.parser.parse(self.request.POST['last_time'])
        all_posts = Post.objects_ext.get_all_visibile_posts(active_author=self.request.user.author, page_author=page_author, reversed=False, min_time=time)
        
        for post in all_posts:
            response_data = {'form': render_to_string("post/post_form.html", {"post_form": PostForm()})}
            response_data["post"] = render_to_string("post/post.html", {"post": post, "MEDIA_URL": settings.MEDIA_URL})
            response_data["post"] += render_to_string("post/post_footer.html", {"post": post})
            response_data["created_guid"] = post.guid
            posts.append(response_data)

        if time is not None:
            all_comments = Comment.objects.filter(pubDate__gt=time, post__in=all_posts)
        else:
            all_comments = Comment.objects.filter(post__in=all_posts)

        for comment in all_comments:
            response_data = {'form': render_to_string("comment/comment_form.html", {"comment_form": CommentForm()})}
            response_data["comment"] = render_to_string("comment/comment.html", {"comment": comment})
            response_data["postGUID"] = comment.post.guid
            comments.append(response_data)

        return JsonResponse({'posts': posts, 'comments': comments, 'time': datetime.datetime.now(dateutil.tz.tzutc()).isoformat()})


class ProfileUpdateView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileUpdateView, self).dispatch(*args, **kwargs)

    def post(self, request, authorUUID, *args, **kwargs):
        template_name = 'edit_profile.html'
        form_name_in_template = "author_form"
        form_class = ProfileEditForm

        form = form_class(request.POST, request.FILES, instance=self.request.user.author)

        if not form.is_valid():
            response_data = {'form': render_to_string(template_name, {form_name_in_template : form})}
            return JsonResponse(response_data, status=400)

        obj = form.save(commit=True)
        return JsonResponse({}, status=200)


class ProfileStreamView(TemplateView):
    template_name = "profile_stream.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileStreamView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileStreamView, self).get_context_data(**kwargs)
        authorUUID = self.kwargs.get('authorUUID', self.request.user.author.uuid)
        profile_author = Author.objects.filter(uuid=authorUUID)
        context['posts'] = Post.objects_ext.get_profile_visibile_posts(active_author=self.request.user.author, page_author=profile_author)
        context['comment_form'] = CommentForm()
        return context
