from typing import Optional, Union

from .helpers import extract_symbol, set_html_style, to_xml_attrs


class IconsTracker(set):
    def __init__(
        self,
        css_class: str,
        symbol_prefix: str,
        icons_map: dict,
        icons_dir: Optional[str],
    ):
        self.css_class = css_class
        self.symbol_prefix = symbol_prefix
        self.icons_map = icons_map
        self.icons_dir = icons_dir
        super().__init__()

    def get_symbol_id(self, name: str):
        return f"{self.symbol_prefix}{name}"

    def use(
        self,
        name: str,
        size: Optional[Union[str, int]] = None,
        label: Optional[str] = None,
        **attrs,
    ) -> str:
        symbol_id = self.get_symbol_id(name)
        self.add(
            extract_symbol(
                name=name,
                symbol_id=symbol_id,
                svg_content=self.icons_map.get(name),
                icons_dir=self.icons_dir,
            )
        )

        attrs["class"] = f'{attrs.get("class", "")} {self.css_class}'.strip()

        if size:
            attrs["style"] = set_html_style(
                attrs.get("style", ""),
                dict(width=size, height=size),
            )

        if label:
            attrs["aria-label"] = attrs.get("aria-label", label)
            attrs["role"] = attrs.get("role", "img")

        else:
            attrs["aria-hidden"] = attrs.get("aria-hidden", "true")

        attrs = to_xml_attrs(attrs)
        return f'<svg {attrs}><use href="#{symbol_id}"></use></svg>'

    def get_sprite(self):
        if not self:
            return ""

        return (
            '<svg xmlns="http://www.w3.org/2000/svg" style="display:none;">'
            f'{"".join(x for x in self)}</svg>'
        )

    @property
    def is_empty(self):
        return not bool(self)
