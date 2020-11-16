from django import template

register = template.Library()


@register.filter
def resource_as_percent(value):
    factor = 100.0
    if value.endswith('m'):
        factor = 0.1
        value = value[0:-1]
    value = float(value) * factor
    return "{}%".format(value)
