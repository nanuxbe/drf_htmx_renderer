from drf_auto_endpoint.endpoints import Endpoint
from drf_auto_endpoint.router import register

from .models import Category, Product


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

