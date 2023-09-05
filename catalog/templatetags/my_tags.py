from django import template
from django.conf import settings

register = template.Library()


@register.filter
def mediapath(path):
    if path:
        return f"{settings.MEDIA_URL}{path}"
    else:
        return f"{settings.MEDIA_URL}not_image"


# @register.simple_tag
# def mediapath_tag(path):
#     if path:
#         return f"{settings.MEDIA_URL}{path}"
#     else:
#         return f"{settings.MEDIA_URL}not_image.png"
