from .constants import SVG_SPRITE_PLACEHOLDER
from .settings import appsettings
from .tracker import IconsTracker


class SvgiconMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request._svgicon_tracker = IconsTracker(
            css_class=appsettings.CSS_CLASS,
            symbol_prefix=appsettings.SYMBOL_PREFIX,
            icons_map=appsettings.ICONS,
            icons_dir=appsettings.ICONS_DIR,
        )
        response = self.get_response(request)

        if not response.get("Content-Type", "").startswith("text/html"):
            return response

        if request._svgicon_tracker.is_empty:
            return response

        content = response.content.decode(response.charset)
        if SVG_SPRITE_PLACEHOLDER not in content:
            return response

        sprite_block = request._svgicon_tracker.get_sprite()
        content = content.replace(SVG_SPRITE_PLACEHOLDER, sprite_block)
        response.content = content.encode(response.charset)
        return response
