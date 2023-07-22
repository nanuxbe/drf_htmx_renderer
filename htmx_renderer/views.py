from functools import wraps

from rest_framework.response import Response
from rest_framework.routers import APIRootView as DRFRootView
from rest_framework.viewsets import ModelViewSet as DRFModelViewSet
from drf_auto_endpoint.decorators import bulk_action


def redirect_success(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        response['HX-redirect'] = f'{request.path}../'
        return response

    return wrapper


class APIRootView(DRFRootView):

    def get_template_names(self):
        if self.request.headers.get('Hx-Request', False):
            base_dir = 'htmx'
        else:
            base_dir = 'html'

        return [
            f'{base_dir}/root.html',
            'html/base.html'
        ]


class ModelViewSet(DRFModelViewSet):

    def get_template_names(self):
        print(self.action)
        if self.request.headers.get('Hx-Request', False):
            if 'partials' in self.request.query_params:
                return ['htmx/partial.html']
            base_dir = 'htmx'
        else:
            base_dir = 'html'
        return [
            f'{base_dir}/{self.endpoint.model.__module__}_{self.endpoint.model.__name__}_{self.action}.html',
            f'{base_dir}/{self.endpoint.model.__name__}_{self.action}.html',
            f'{base_dir}/{self.action}.html',
            'html/base.html'
        ]

    @bulk_action('GET')
    def new(self, request):
        return Response()

    def update(self, request, pk, **kwargs):
        return super().update(request, pk, **kwargs)

    def create(self, request, **kwargs):
        return super().create(request, **kwargs)
