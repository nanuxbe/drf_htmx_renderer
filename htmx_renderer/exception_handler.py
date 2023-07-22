from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def render_html_errors(exc, context):
    if isinstance(exc, ValidationError):
        print('----')
        print(exc.detail, exc.get_full_details())
        print(context)

        context['errors'] = exc.detail

        return Response({'errors': exc.detail}, template_name='htmx/errors.html')

    return exception_handler(exc, context)

