import os
from functools import lru_cache
from os.path import join
from typing import Optional, Tuple

from django.contrib.staticfiles import finders

try:
    from lxml import ET
except ImportError:
    import xml.etree.ElementTree as ET


symbol_attrs = ("viewbox", "width", "height")


def xml_removens(elem):
    tag = elem.tag.split("}")[-1]  # Remove namespace
    new_elem = ET.Element(tag, **elem.attrib)
    new_elem.text, new_elem.tail = elem.text, elem.tail
    new_elem.extend(map(xml_removens, elem))
    return new_elem


def extract_svg_symbol(svg_content: str, symbol_id: str) -> Tuple[str, str]:
    root = xml_removens(ET.fromstring(svg_content))
    content = "".join(ET.tostring(child, encoding="unicode") for child in root)

    normalized_attrs = {k.lower(): v for k, v in root.attrib.items()}
    attrs = {
        attr: normalized_attrs[attr]
        for attr in symbol_attrs
        if attr in normalized_attrs
    }

    attrs_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    symbol = f'<symbol id="{symbol_id}" {attrs_str}>{content}</symbol>'

    return symbol


@lru_cache
def extract_symbol(
    name: str,
    symbol_id: str,
    svg_content: Optional[str] = None,
    icons_dir: Optional[str] = None,
) -> Tuple[str, str]:
    icon_path = None
    if not svg_content:
        icon_filename = "%s.svg" % name
        if icons_dir:
            icon_path = join(icons_dir, icon_filename)
        else:
            icon_path = finders.find(join("svgicons", icon_filename))
            if not icon_path:
                raise PermissionError(
                    "Unable to locate '%s' svg file in paths: %s"
                    % (
                        icon_filename,
                        ", ".join(finders.searched_locations),
                    )
                )

        if not os.access(icon_path, os.R_OK):
            raise PermissionError(f"Unable to access svg file {icon_path}")

        with open(icon_path, mode="r") as f:
            svg_content = f.read()

        if not svg_content:
            raise ValueError("Empty SVG file on %s" % icon_path)

    try:
        return extract_svg_symbol(svg_content, symbol_id)
    except Exception:
        if icon_path:
            print("Invalid SVG file %s" % icon_path)
        print("Invalid SVG content for %s" % name)
        raise


def to_xml_attrs(attrs: dict) -> str:
    r = ""
    for k, v in attrs.items():
        k = k.replace("_", "-")
        r += f'{k}="{v}" '
    return r.strip()


def html_style_to_dict(style: str) -> dict:
    r = dict()
    for x in style.split(";"):
        if not x:
            continue
        k, v = x.strip().split(":")
        r[k] = v
    return r


def set_html_style(style: str, new_style: dict) -> str:
    r = html_style_to_dict(style)

    for k, v in new_style.items():
        r[k] = v

    return ";".join(f"{k}:{v}" for k, v in r.items())


@lru_cache
def generate_css(classname: str, width: str, height: str) -> str:
    if not classname:
        return ""

    return (
        f"<style>.{classname}{{"
        f"width:{width};"
        f"height:{height};"
        "fill:currentColor;"
        "vertical-align:middle;"
        "}</style>"
    )
