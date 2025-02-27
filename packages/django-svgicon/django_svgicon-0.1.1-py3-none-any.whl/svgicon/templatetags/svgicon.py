from django import template
from django.utils.safestring import mark_safe

from ..constants import SVG_SPRITE_PLACEHOLDER
from ..helpers import generate_css
from ..settings import appsettings

register = template.Library()


@register.simple_tag(name=appsettings.TAGS["ICON"], takes_context=True)
def icon(context, name, **kwargs):
    """
    Usage: {% icon "menu" id="menu-icon" %}
    """

    request = context["request"]
    return mark_safe(request._svgicon_tracker.use(name, **kwargs))


@register.simple_tag(name=appsettings.TAGS["STYLE"])
def svgicon_style():
    return mark_safe(
        generate_css(
            classname=appsettings.CSS_CLASS,
            width=appsettings.WIDTH,
            height=appsettings.HEIGHT,
        )
    )


@register.simple_tag(name=appsettings.TAGS["SPRITE"])
def svgicon_sprite():
    return mark_safe(SVG_SPRITE_PLACEHOLDER)
