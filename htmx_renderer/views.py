from functools import wraps

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet as DRFModelViewSet
from drf_auto_endpoint.decorators import bulk_action


def redirect_success(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        response['HX-redirect'] = f'{request.path}../'
        return response

    return wrapper


class ModelViewSet(DRFModelViewSet):

    @bulk_action('GET')
    def new(self, request):
        return Response()
