from django.conf import settings


class SvgiconSettings:
    DEFAULT_TAGS = dict(
        ICON="icon",
        SPRITE="svgicon_sprite",
        STYLE="svgicon_style",
    )
    DEFAULT_ICONS = dict()
    DEFAULT_SYMBOL_PREFIX = "icon-"
    DEFAULT_WIDTH = "1em"
    DEFAULT_HEIGHT = "1em"
    DEFAULT_CSS_CLASS = "svgicon"

    @property
    def TAGS(self):
        usertags = getattr(settings, "SVGICON_TAGS", {})
        return {k: usertags.get(k, v) for k, v in self.DEFAULT_TAGS.items()}

    @property
    def ICONS(self):
        return getattr(settings, "SVGICON_ICONS", self.DEFAULT_ICONS)

    @property
    def WIDTH(self):
        return getattr(settings, "SVGICON_WIDTH", self.DEFAULT_WIDTH)

    @property
    def HEIGHT(self):
        return getattr(settings, "SVGICON_HEIGHT", self.DEFAULT_HEIGHT)

    @property
    def CSS_CLASS(self):
        return getattr(settings, "SVGICON_CSS_CLASS", self.DEFAULT_CSS_CLASS)

    @property
    def ICONS_DIR(self):
        return getattr(settings, "SVGICON_ICONS_DIR", None)

    @property
    def SYMBOL_PREFIX(self):
        return getattr(
            settings,
            "SVGICON_SYMBOL_PREFIX",
            self.DEFAULT_SYMBOL_PREFIX,
        )


appsettings = SvgiconSettings()
