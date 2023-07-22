from urllib.parse import quote_plus

from django.apps import apps
from django.template.defaulttags import register
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.utils.safestring import mark_safe


def _field_by_name(fields, field_name):
    return [f for f in fields if f.get('name', None) == field_name][0]


@register.filter
def field_by_name(fields, field_name):
    return _field_by_name(fields, field_name)


@register.filter
def url(action, id):
    return action['url'].replace(':id', str(id))


@register.filter
def app_name(full_name):
    return full_name.split('.')[0]


@register.filter
def to_str(obj):
    if isinstance(obj, dict):
        return obj.get('__str__', '')
    return str(obj)


@register.filter
def get(record, field_name):
    try:
        return record.get(field_name)
    except AttributeError:
        print(type(record))
        return ''


@register.simple_tag(takes_context=True)
def qs(context, *ignore):
    ignored = ('partials', ) + ignore

    qs = [f'{param}={quote_plus(value)}'
          for param, value in context['request'].GET.items()
          if param not in ignored]

    return f"?{'&'.join(qs)}"


@register.inclusion_tag('fields/_include_field.html', takes_context=True)
def include_field_widget(context, is_editable=False, is_filter=False, **kwargs):
    if 'field_name' in kwargs:
        field_name = kwargs['field_name']
        context['field_name'] = field_name
    elif 'field_name' in context:
        field_name = context['field_name']
    else:
        raise Exception('please provide a field name')

    print(field_name)

    context['field'] = _field_by_name(context['meta']['fields'], field_name)

    if 'metadata' in context:
        context['field'].update(context['metadata'])
    if 'metadata' in kwargs:
        context['field'].update(kwargs['metadata'])

    print(context['field'])

    try:
        template_name = f'fields/{context["field"]["widget"]}-widget.html'
        get_template(template_name)
    except TemplateDoesNotExist:
        template_name = 'fields/_default-widget.html'

    context['to_include'] = template_name
    context['is_editable'] = is_editable or field_name in context['meta']['list_editable']
    context['is_filter'] = is_filter
    return context


@register.filter
def fk_str(record, field):
    # Model = apps.get_model(
    #     *field['extra']['related_model'].split('/')
    # )
    # return Model.objects.get(pk=record[field['name']]).__str__()

    return record[field['name']]['__str__']


@register.simple_tag(takes_context=True)
def hx_attrs(context):
    rv = ''

    if 'id' in context.get('params', {}):
        rv += f' id="{context["params"]["id"]}" '
    if context.get('params', {}).get('oob', False):
        rv += ' hx-swap-oob="true" '

    return mark_safe(rv)


@register.simple_tag()
def hx_swap(what='outerHTML', duration='.3s', push_url=False):
    if push_url in ['true', 'True', True]:
        push_url = 'true'
    elif push_url in ['false', 'False', False]:
        push_url = 'false'
    # TODO if push_url is True, replace with requested url without "partials" query param
    return mark_safe(f'hx-swap="{what} swap:{duration}" hx-push-url="{push_url}"')


@register.simple_tag(takes_context=True)
def record_name(context):
    return context['__str__']


@register.filter
def select_list(field, selected=None):
    Model = apps.get_model(
        *field['extra']['related_model'].split('/')
    )
    rv = ((str(r.pk), r.__str__()) for r in Model.objects.all())
    return rv


@register.filter('range')
def range_filter(number):
    return [i for i in range(number)]


@register.filter
def range1(number):
    return [i for i in range(1, number + 1)]


@register.filter
def range_to(number, count):
    return [i for i in range(number - count + 1, number + 1)]


@register.filter
def range_around(number, count):
    return [i for i in range(number - count, number + 1 + count)]


@register.filter
def comp_id(active_filter, value):
    rv = active_filter == value
    return rv


@register.inclusion_tag('htmx/include.html', takes_context=True)
def include_with_context_as_record(context, path):
    context['record'] = context
    context['path'] = path
    context['htmx'] = True
    return context


@register.inclusion_tag('htmx/include.html', takes_context=True)
def include_htmx_partial(context, template_name):
    candidates = [
        f'htmx/partials/{template_name}.html',
        None,
    ]
    if 'model' in context.get('meta', {}):
        candidates.insert(0, f'htmx/partials/{context["meta"]["model"]}_{template_name}.html')
        if 'app' in context.get('meta', {}):
            candidates.insert(0, f'htmx/partials/{context["meta"]["app"]}_{context["meta"]["model"]}_{template_name}.html'),

    while (template := candidates.pop(0)) is not None:
        try:
            get_template(template)
            context['path'] = template
            return context
        except TemplateDoesNotExist:
            pass

    raise TemplateDoesNotExist(template_name)

