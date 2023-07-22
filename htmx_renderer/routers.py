from drf_auto_endpoint.router import EndpointRouter

from .views import APIRootView

class HTMXRendererRouter(EndpointRouter):
    APIRootView = APIRootView
