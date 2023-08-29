from django import template
from django.conf import settings

register = template.Library()


@register.filter
def mediapath(path):
    return f"{settings.MEDIA_URL}{path}"


@register.simple_tag
def mediapath_tag(path):
    return f"{settings.MEDIA_URL}{path}"
