# django-svgicon

[![pypi](https://img.shields.io/pypi/pyversions/django-svgicon.svg)](https://pypi.python.org/pypi/django-svgicon)

SVG icons for Django.

- Automatic SVG Sprite generator based on icons used in the page
- Read icons from directory and Python dict
- Customizable template tags
- In-memory cache

## Requirements
- Django >= 5
- Python >= 3.10

## Installation

```bash
pip install django-svgicon
```

To parse SVG files faster, install `lxml` [optional]:
```bash
pip install lxml
```

## Configuration
Add `svgicon` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    "svgicon",
    "YOUR_APP",
    ...
)
```

Add the middleware:
```python
MIDDLEWARE = [
    ...
    "svgicon.middleware.SvgiconMiddleware",
    ...
]
```

## Usage

1. Put the icons in `yourapp/static/svgicons`, for example:
```bash
yourapp/static/svgicons/menu.svg
```

2. Use it in your templates like this:
```html
{% load svgicon %}
<!DOCTYPE html>
<html>
  <head>
    <title>The App</title>
    {% svgicon_style %} <!-- before your app.css -->
  </head>
  <body>
    {% svgicon_sprite %}

    <main>
      <p>Click on the {% icon "menu" %} button to open the menu.</p>
      <button>{% icon "menu" %}</button>
    </main>
  </body>
</html>
```

For more examples like changing size or setting `aria-label`, follow the 
[demo template](demo/theapp/templates/index.html).

## Settings
```python
# By default, svgicon searches for icons using Django's static finders, 
# unless you specify a directory like this
SVGICON_ICONS_DIR = BASE_DIR / "myicons"

# Load icons from dict
SVGICON_ICONS = dict(
    square=(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
        '<path d="M3,3V21H21V3" />'
        "</svg>"
    ),
)

# svgicon uses '1em' width and height for icons, which are relative to the parent's
# font-size.
SVGICON_WIDTH = '1em'
SVGICON_HEIGHT = '1em'

# Default CSS class for each icon
SVGICON_CSS_CLASS = 'svgicon'

# SVG symbol id prefix
SVGICON_SYMBOL_PREFIX = 'icon-'

# svgicon template tag names
SVGICON_TAGS = dict(
    ICON="icon",
    SPRITE="svgicon_sprite",
    STYLE="svgicon_style",
)
```

To auto-load svgicon without mentioning `{% load svgicon %}`,
modify template settings like this:
```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            ...
            "builtins": ["svgicon.templatetags.svgicon"], # add this 
            ...
        },
    },
]
```
