# Django Meta OG


HTML Meta tags [OpenGraph](https://ogp.me/) for [Django](https://www.djangoproject.com/).
The project uses the project [DjangoCMS Meta OG](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og) project.

### Install

`pip install django-meta-og`


Add into settings.py:

```python
from django.utils.translation import gettext_lazy as _

INSTALLED_APPS = [
    "django_meta_og",
    ...
]

TEMPLATES  = [
    {"OPTIONS": {
            "context_processors": [
                "django_meta_og.context_processors.meta",
                ...
            ]
        }
    }
]
```

Add into the templates:

```django
{% load django_meta_og %}
{% django_meta_og_prefix as og_prefix %}
<head{% if og_prefix %} prefix="{{ og_prefix }}"{% endif %}>
    {% include "django_meta_og/header_meta.html" %}
```

The result can be:

```html
<head prefix="og: https://ogp.me/ns#">
    <meta property="og:type" content="website" />
    <meta property="og:title" content="The Title" />
    <meta property="og:url" content="https%3A%2F%2Fexample.com%2F" />
    ...
</head>
```

### Prefix for Meta tags in template

Some Meta tags may already be defined in the template. Their prefix is ​​included in the prefix list via the definition in settings:

```python
# Example of tag definition already used in the templates.
META_OG_PREFIX_IN_TEMLATES = (
    ("og", "https://ogp.me/ns#"),
    ("article", "https://ogp.me/ns/article#"),
)
```

### Dynamic content

Special values ​​can be replaced with some content.
A list of these values ​​is provided in the form in the item administration.

```python
# Dynamic content - Key replacement for specific content.
PAGE_META_OG_DYNAMIC_CONTENT = {
    "ogc:page_url": (
        "django_meta_og.dynamic_content.get_page_url",
        _("Set the page absolute URL (together with parameters)."),
    ),
}
```

### Admininstration

You can enter any Meta values. These are entered in three levels - Namespace, Property and Content.

#### Namespace

![Namespace list](https://gitlab.nic.cz/django-apps/django-meta-og/-/raw/main/screenshots/django-admin-namespace-list.png "Namespace list")

![Namespace form](https://gitlab.nic.cz/django-apps/django-meta-og/-/raw/main/screenshots/django-admin-namespace-form.png "Namespace form")

#### Property

![Property list](https://gitlab.nic.cz/django-apps/django-meta-og/-/raw/main/screenshots/django-admin-property-list.png "Property list")

![Property form](https://gitlab.nic.cz/django-apps/django-meta-og/-/raw/main/screenshots/django-admin-property-form.png "Property form")

#### Content

![Content list](https://gitlab.nic.cz/django-apps/django-meta-og/-/raw/main/screenshots/django-admin-content-list.png "Content list")

![Content form](https://gitlab.nic.cz/django-apps/django-meta-og/-/raw/main/screenshots/django-admin-content-form.png "Content form")

### License

BSD License
