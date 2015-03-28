from rest_framework import serializers
from Hindlebook.models import Node, Author
from Hindlebook.utilites import Logger
from api.requests import ProfileRequestFactory
from api.serializers import ProfileSerializer

logger = Logger()


def getForeignProfile(uuid, node):
    """
    Fetches the profile for the foreign user specified by uuid from the specfied node
    """
    author = None

    request = ProfileRequestFactory.create(node)
    response = request.get(uuid)

    if(response.status_code != 200):
        # Node not reachable or some other mishap
        logger.log(response.content)
        logger.log("HTTP %s returned from %s on friend request echo." % (response.status_code, node.host))
        return None

    data = response.json()


def get_node(node_string):
    """
    Fetches the corresponding node matching the given string
    """
    node = Node.objects.filter(host=node_string).first()
    if node is None:
        logger.log("Unknown host '%s' during serialization, throwing exception" % node_string)
        raise serializers.ValidationError('Invalid or Unknown Host: %s' % node_string)

    return node


def get_author(author_data):
    """
    Gets the Author, creats a new one if necesary
    """
    if author_data is None:
        return None

    # Get Author/Host info
    uuid = author_data.get('uuid', )
    host = author_data.get('node')
    username = author_data.get('username')

    node = get_node(host)

    author = Author.objects.filter(uuid=uuid).first()
    if author is None:
        # New foreign author
        profile_data = getForeignProfile(uuid, node)



        github_id = profileJSON.get('github_id', "")
        about = profileJSON.get('about', "")
        username = profileJSON.get('username', username)
        avatar = "foreign_avatar.jpg"

        author = Author.objects.create(uuid=uuid, node=node, username=username,
                                       github_id=github_id, about=about, avatar=avatar)

    elif author.user is None:
        # Existing Foreign Author, update them
        profileJSON = getForeignProfile(uuid, node)
        if profileJSON is None:
            profileJSON = {}

        github_id = profileJSON.get('github_id', author.github_id)
        about = profileJSON.get('about', author.about)
        username = profileJSON.get('username', username)
        author.avatar = "foreign_avatar.jpg"
        author.username = username
        author.github_id = github_id
        author.about = about
        author.save()

    return author
