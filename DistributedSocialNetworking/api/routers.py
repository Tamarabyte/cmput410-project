from rest_framework.routers import Route, DynamicDetailRoute, SimpleRouter

class CustomSimpleRouter(SimpleRouter):
    """
    A router for read-only APIs, only supports retrieving the list (ex. '/users' or a single user ex. '/user/id')
    """
    routes = [
        Route(
            url=r'^{prefix}s$',
            mapping={'get': 'list'},
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
           mapping={'get': 'retrieve',
                    'put' : 'update'},
           name='{basename}-detail',
           initkwargs={'suffix': 'Detail'}
        ),
        DynamicDetailRoute(
            url=r'^{prefix}/{lookup}/{methodnamehyphen}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        )
    ]