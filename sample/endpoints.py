import json

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse

from drf_auto_endpoint.decorators import custom_action, bulk_action
from drf_auto_endpoint.endpoints import Endpoint
from drf_auto_endpoint.router import register
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from .models import Category, Product, Project, Todo, MoodTracker, Feeling, Caring


@register
class CategoryEndpoint(Endpoint):
    model = Category
    list_display = ('name', )
    search_fields = ('name', )
    ordering_fields = ('name', )


@register
class ProductEndpoint(Endpoint):
    model = Product
    list_display = ('name', 'category', 'price', )
    search_fields = ('name', )
    filter_fields = ('category_id', )
    ordering_fields = ('name', 'price', )


@register
class UserEndpoint(Endpoint):
    model = get_user_model()
    read_only = True
    list_me = False


@register
class ProjectEndpoint(Endpoint):
    model = Project
    list_display = ('name', 'state', 'owner')

    @custom_action('POST', icon_class='fa fa-arrow-right', btn_class='btn btn-outline-success')
    def start(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        if obj.state not in ('draft', 'finished'):
            raise MethodNotAllowed(request.method)
        obj.state = 'running'
        obj.save()
        data = self.get_serializer(obj).data
        return Response(data)


@register
class TodoEndpoint(Endpoint):
    model = Todo
    list_display = ('is_done', 'description')
    list_editable = ('is_done', )
    filter_fields = ('is_done', )

    @bulk_action(method='DELETE')
    def clear(self, request):
        Todo.objects.filter(is_done=True).delete()

        qs = Todo.objects.all()
        serializer = self.get_serializer()(qs, many=True)
        response = Response({'results': serializer.data})
        response['HX-Location'] = json.dumps({
            "path": reverse('sample/todos-list'),
            "target": "#main",
            "swap": "outerHTML",
        })

        return response


@register
class MoodTrackerEndpoint(Endpoint):
    model = MoodTracker
    list_display = ('name', 'description', 'date', 'emote, feels, cares')
    list_editable = ('name', 'description', 'emote, feels, cares')


@register
class FeelingEndpoint(Endpoint):
    model = Feeling
    list_display = ('feels')
    list_editable = ('feels')


@register
class CareEndpoint(Endpoint):
    model = Caring
    list_display = ('cares')
    list_editable = ('cares')
