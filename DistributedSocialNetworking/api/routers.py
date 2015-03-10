from rest_framework.routers import Route, DynamicDetailRoute, SimpleRouter

class ReadOnlyRouter(SimpleRouter):
    """
    A router for read-only APIs, only supports retrieving the list (ex. '/users' or a single user ex. '/user/id')
    """
    # test
    routes = [
        Route(
            url=r'^{prefix}s$',
            mapping={'get': 'list'},
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
           mapping={'get': 'retrieve'},
           name='{basename}-detail',
           initkwargs={'suffix': 'Detail'}
        ),
        DynamicDetailRoute(
            url=r'^{prefix}/{lookup}/{methodnamehyphen}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        )
    ]