# Settings for Nodes

HINDLEBOOK = {
    'host': "hindlebook.tamarabyte.com",
    'username': "hindlebook.tamarabyte.com",
    'password': "test",
    'port': ''
}

DEV_HINDLEBOOK = {
    'host': "dev.tamarabyte.com",
    'username': "hindlebook.tamarabyte.com",
    'password': "test",
    'port': ''
}


from api.requests.public_posts_factory import PublicPostsRequestFactory
from api.requests.visible_posts_factory import VisiblePostsRequestFactory
from api.requests.authored_posts_factory import AuthoredPostsRequestFactory
from api.requests.post_factory import PostRequestFactory
from api.requests.friend_request_factory import FriendRequestFactory
from api.requests.friend_query_factory import FriendQueryRequestFactory
