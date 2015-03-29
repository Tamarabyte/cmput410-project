from rest_framework import serializers
from Hindlebook.models import Node, Author
from Hindlebook.utilites import Logger
from api.requests import ProfileRequestFactory
from api.serializers import ProfileSerializer

logger = Logger()


def get_foreign_profile_data(uuid, node):
    """
    Fetches the profile for the foreign user specified by uuid from the specfied node
    """
    request = ProfileRequestFactory.create(node)
    response = request.get(uuid)

    if(response.status_code != 200):
        # Node not reachable or some other mishap
        logger.log(response.content)
        logger.log("HTTP %s returned from %s on profile request." % (response.status_code, node.host))
        print("HTTP %s returned from %s on profile request." % (response.status_code, node.host))
        return {}

    return response.json()


def get_node(node_string):
    """
    Fetches the corresponding node matching the given string
    """
    node = Node.objects.filter(host=node_string).first()
    if node is None:
        print
        logger.log("Unknown host '%s' during serialization, throwing exception" % node_string)
        raise serializers.ValidationError('Invalid or Unknown Host: %s' % node_string)

    return node


def get_author(uuid, host):
    """
    Gets the Author, creats a new one if necesary
    """
    if not uuid or not host:
        return None

    # Get Author
    author = Author.objects.filter(uuid=uuid).first()

    if author is None:
        # New foreign author, create them
        profile_data = get_foreign_profile_data(uuid, get_node(host))
        serializer = ProfileSerializer(data=profile_data)

        try:
            serializer.is_valid(raise_exception=True)
            author = serializer.save()

            github_id = profile_data.get("github_username", None)
            if github_id:
                author.github_id = github_id
                author.save()

            about = profile_dats.get("bio", None)
            if about:
                about.about = about
                author.save()

        except:
            print("Debug: returning None for Author in utils.py")
            author = None

    elif author.user is None:
        # Existing Foreign Author, update them
        profile_data = get_foreign_profile_data(uuid, get_node(host))
        serializer = ProfileSerializer(author, data=profile_data)
        serializer.is_valid(raise_exception=True)
        author = serializer.save()

        print("profile data")
        print(profile_data)

        github_id = profile_data.get("github_username", None)
        if github_id:
            author.github_id = github_id
            author.save()

        about = profile_data.get("bio", None)
        if about:
            about.about = about
            author.save()

    return author
