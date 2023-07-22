import json
import math

from django.conf import settings
from django.http import Http404
from django.urls import reverse

from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import TemplateHTMLRenderer as DRFTemplateHTMLRenderer

from drf_auto_endpoint.metadata import AutoMetadata


class TemplateHTMLRenderer(DRFTemplateHTMLRenderer):

    meta_data_adapter = AutoMetadata()
    exception_template_names = [
        'htmx/%(status_code)d_errors.html',
    ]

    REDIRECT_ON_SUCCESS = [
        'create',
        'update',
        'destroy',
    ]

    def _handle_exception_context(self, context, data, response):
        if not response.exception:
            return

        context['errors'] = {
            field['name']: response.data[field['name']]
            for field in response.data['meta']['fields']
            if field['name'] in data
        }

    def _add_single_object_serializer(self, context, view):
        if 'results' in context:
            # not single object
            return

        try:
            try:
                obj = view.get_object()
            except AssertionError:
                # actually no object at all
                obj = None
            context['serializer'] = view.get_serializer(obj)
        except AttributeError:
            # Object not applicable
            return
        except Http404:
            # after delete
            return

    def _add_ordering_data(self, context, request, view):
        current_ordering = None
        if hasattr(view, 'endpoint'):
            endpoint = view.endpoint
            context['meta']['app'] = endpoint.__module__
            if hasattr(endpoint, 'model') and endpoint.model is not None:
                context['meta']['model'] = endpoint.model.__name__
                if len(endpoint.model._meta.ordering) == 1:
                    current_ordering = endpoint.model._meta.ordering[0]

        current_ordering = request.GET.get('ordering', current_ordering)
        context['current_ordering'] = current_ordering

    def _add_pagination_data(self, context, request, view):
        if context.get('next', None) is None and context.get('previous', None) is None:
            # no pagination
            return

        context['is_paginated'] = True
        if issubclass(view.pagination_class, PageNumberPagination):
            context['show_pages'] = True
            context['current_page'] = int(request.GET.get(view.pagination_class.page_query_param, 1))
            context['page_query_param'] = view.pagination_class.page_query_param
            page_size = request.GET.get(
                view.pagination_class.page_size_query_param,
                view.pagination_class.page_size
            )
            context['total_pages'] = math.ceil(int(context['count']) / int(page_size))
            context['pages_around'] = getattr(settings, 'PAGINATION_PAGES_AROUND', 3)

    def _add_filters_data(self, context, request):
        if 'filter_fields' not in context.get('meta', {}):
            return

        context['active_filters'] = {}

        for field_name in context['meta']['filter_fields']:
            param_value = request.GET.get(field_name, '')
            context['active_filters'][field_name] = param_value

    def _redirect_on_success(self, request, view, response):
        print('SUCCESS')
        if not hasattr(view, 'action'):
            return

        if view.action in self.REDIRECT_ON_SUCCESS and 200 <= response.status_code < 300:
            # response.status_code = 303
            # response['location'] = f'{request.path}../'
            response['HX-Location'] = json.dumps({
                "path": reverse(f'{view.basename}-list'),
                "target": "#main",
                "swap": "outerHTML",
            })

    def get_template_context(self, data, renderer_context):
        context = super().get_template_context(data, renderer_context)
        if context is None:
            context = {}

        request = renderer_context['request']
        response = renderer_context['response']

        view = renderer_context['view']

        context['meta'] = self.meta_data_adapter.determine_metadata(
            request,
            view
        )
        context['request'] = request
        context['view'] = view

        self._handle_exception_context(context, data, response)
        self._add_single_object_serializer(context, view)
        self._add_ordering_data(context, request, view)
        self._add_pagination_data(context, request, view)
        self._add_filters_data(context, request)
        self._redirect_on_success(request, view, response)

        partials = request.GET.get('partials', '').split(',')
        context['templates'] = {f'./partials/{p}.html': {'oob': bool(i)}
                                for i, p in enumerate(partials)}

        return context

