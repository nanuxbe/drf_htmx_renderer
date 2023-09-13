from copy import deepcopy
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
    import pprint
    print(type(context))
    print('**********************')
    new_context = dict({
        k: context.get(k, None)
        for k in ('record', 'meta', 'request', 'serializer', 'view')
    })
    if 'field_name' in kwargs:
        field_name = kwargs['field_name']
        new_context['field_name'] = field_name
        print('field_name from kwargs')
    elif 'field_name' in context:
        field_name = context['field_name']
        new_context['field_name'] = field_name
        print('field_name from context')
    else:
        raise Exception('please provide a field name')

    try:
        print(f'trying to extract {field_name} from {[f.get("name", "") for f in context["meta"]["fields"]]}')
        metadata = deepcopy(_field_by_name(context['meta']['fields'], field_name))
    except IndexError:
        print(f'could not find {field_name}')
        # Unnamed field, probably a fieldset or tabset
        metadata = {}

    print('metadata', metadata)

    if 'field' in kwargs:
        metadata.update(kwargs['field'])
    elif 'field' in context:
        metadata.update(deepcopy(context['field']))

    print('-')

    if 'class' not in metadata:
        metadata['class'] = kwargs.get('class', '')
    if 'showLabel' in kwargs:
        metadata['showLabel'] = kwargs['showLabel']
    elif 'showLabel' not in metadata:
        metadata['showLabel'] = True
    new_context['field'] = metadata
    print('--')
    pprint.pprint(new_context['field'])

    try:
        template_name = f'fields/{metadata["widget"]}-widget.html'
        get_template(template_name)
        print(f'rendering {template_name}')
    except TemplateDoesNotExist:
        template_name = 'fields/_default-widget.html'
        print('rendring default widget')

    new_context['to_include'] = template_name
    new_context['is_editable'] = is_editable or field_name in context['meta']['list_editable']
    new_context['is_filter'] = is_filter
    return new_context


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
def include_with_context_as_record(context, template_name, **kwargs):
    context['record'] = context['serializer'].data
    # context['path'] = path
    context['htmx'] = True
    context.update(kwargs)
    return _render_partial_template(context, template_name)


def _render_partial_template(context, template_name):
    candidates = [
        f'htmx/partials/{template_name}.html',
        None,
    ]

    try:
        path, filename = template_name.rsplit('/', 1)
    except ValueError:
        path = None
        filename = template_name

    if 'model' in context.get('meta', {}):
        candidates.insert(0, 'htmx/partials/{}{}_{}.html'.format(
            f'{path}/' if path is not None else '',
            context["meta"]["model"],
            filename
        ))
        if 'app' in context.get('meta', {}):
            app = context["meta"]["app"].rsplit('.', 1)[0]
            candidates.insert(0, 'htmx/partials/{}{}_{}_{}.html'.format(
                f'{path}/' if path is not None else '',
                app,
                context["meta"]["model"],
                filename
            ))

    print('---- PARTIAL CANDIDATES ---', candidates)
    while (template := candidates.pop(0)) is not None:
        try:
            get_template(template)
            context['path'] = template
            return context
        except TemplateDoesNotExist:
            pass

    raise TemplateDoesNotExist(template_name)


@register.inclusion_tag('htmx/include.html', takes_context=True)
def include_htmx_partial(context, template_name):
    return _render_partial_template(context, template_name)


@register.filter
def in_m2m_value(id, value):
    if value in ('', None, []):
        return False
    rv = str(id) in [str(x['pk']) for x in value]
    print(id, value, rv)
    return rv
