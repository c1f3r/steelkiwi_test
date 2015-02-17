from django import template

register = template.Library()


@register.filter(name='get_next')
def add_class(value):
    return value[value.find('?next=') + len('?next='):-1] + '/'