# DRF HTMX Renderer

`DRF HTMX Renderer` is a (renderer)[https://www.django-rest-framework.org/api-guide/renderers/] for [Django REST Framework](https://www.django-rest-framework.org/).

In the vain of the browsable API or the admin renderer shipped with DRF, it allows for browsing the API directly in your browser and making it fully human-friendly.

To learn more about this project, you can watch [this talk](https://program.europython.eu/europython-2023/talk/BRY8JS/) - Slides available [here](https://slides.levit.be/ep2023/).

The aim of the project is to provide a customizable and extendable interface for data management that can be presented to the final user.

## Install

### With pip

```
pip install drf-htmx-renderer
```

### From github

```
git clone git@github.com:nanuxbe/drf_htmx_renderer.git
cd drf_htmx_renderer
pip install -e .
pip install -r requirements-dev.txt

python manage.py runserver
```

## Settings

Add these to Django `settings.py`

```python
DRF_AUTO_METADATA_ADAPTER = 'htmx_renderer.adapters.HTMXEndpointAdapter'
DRF_AUTO_BASE_SERIALIZER = 'htmx_renderer.serializers.HTMXModelSerializer'
DRF_AUTO_BASE_VIEWSET = 'htmx_renderer.views.ModelViewSet'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'htmx_renderer.renderers.TemplateHTMLRenderer',
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}
```

Add `htmx_renderer` in to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...

    # API
    'rest_framework',
    'drf_auto_endpoint',
    'htmx_renderer',

    # TEMPLATES
    'bootstrap5',
    'mathfilters',
]
```

## URLs

Add this to the main `urls.py`

```python
from drf_auto_endpoint.router import router

urlpatterns = [
    ...
    path('api/v1/', include(router.urls)),
    ...
]
```

## Getting started

### Create an endpoint for your model

Inside `<your_app>/endpoints.py` create an endpoint:

```python
from drf_auto_endpoint.endpoints import Endpoint
from drf_auto_endpoint.router import register

from .models import MyModel


@register
class MyModelEndpoint(Endpoint):
    model = MyModel
```

Restart Django's development serve and point it to http://localhost:8000/api/v1/

For further customization of your endpoint, refer to [DRF-Schema-Adapter's documentation](https://drf-schema-adapter.readthedocs.io/en/latest/drf_auto_endpoint/endpoint/)

## Building

This project uses standardized `pyproject.toml` for the package. To build it simply invoke

    python -m build

(note, you may need to install `build` package first).

To install package in development mode you can use

    pip install -e .

## Development


### Sample (demo) app

One way to start the development is to run our demo app
and explore examples.
Source code is available in `sample` subdirectory.

#### Create migrations

    python manage.py migrate

#### Start development server

    python manage.py runserver
