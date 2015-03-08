import re
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import Q
from django.shortcuts import render_to_response
from django.core import serializers
from Hindlebook.models import User


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    for term in query_string:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search(request, query=None):
    users = []
    query = query.strip()

    # if starts_with:
    #     user = User.objects.filter(name__istartswith=starts_with)
    # else:
    #             cat_list = Category.objects.all()

    user_query = get_query(query, ['username', 'first_name', 'last_name'])
    users = User.objects.filter(user_query)

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(serializers.serialize("json", users))
    return response