from django.template.defaulttags import register


@register.filter
def count_not_done(records):
    return sum([0 if r['is_done'] else 1 for r in records])


@register.filter
def eq(item, value):
    return item == value
