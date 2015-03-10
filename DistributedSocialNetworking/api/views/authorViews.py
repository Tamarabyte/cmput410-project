from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from hindlebook.models import Snippet
from api.serializers import UserSerializer
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView


class AuthorDetails(APIView):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def allowed_methods(self):
        return ["GET"]

    def get_object(self, uuid):
        try:
            return Post.objects.get(uuid=uuid)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, postID, format=None):
        post = self.get_object(postID)
        serializer = PostSerializer(post)
        return Response(serializer.data)

"""
@csrf_exempt
def snippet_detail(request, pk):


    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
"""