# DjangoCMS Meta OG


HTML Meta tags [OpenGraph](https://ogp.me/) for [DjangoCMS](https://www.django-cms.org/).
The project is based on the [Django Meta OG](https://gitlab.nic.cz/django-apps/django-meta-og) project.

### Install

`pip install djangocms-meta-og`


Add into settings.py:

```python
from django.utils.translation import gettext_lazy as _
import sysconfig

INSTALLED_APPS = [
    "django_meta_og",
    "djangocms_meta_og",
    ...
]

TEMPLATES  = [
    {"OPTIONS": {
            "context_processors": [
                "djangocms_meta_og.context_processors.meta",
                ...
            ]
        }
    }
]

# Path to css and js used in admin form.
STATICFILES_DIRS = [
    os.path.join(sysconfig.get_paths()["purelib"], "djangocms_meta_og")
]
```

For `js` translations add into site urls.py:

```python
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    ...
] + i18n_patterns(
    path('jsi18n/djangocms-meta-og/', JavaScriptCatalog.as_view(packages=['djangocms_meta_og']),
         name='jsi18n_djangocms_meta_og'),
    ...
)
```

Add into the templates:

```django
{% load djangocms_meta_og %}
{% djangocms_meta_og_prefix as og_prefix %}
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
    "ogc:current_page_url": (
        "djangocms_meta_og.dynamic_content.get_current_page_url",
        _("Set the page absolute URL."),
    ),
    "ogc:current_page_title": (
        "djangocms_meta_og.dynamic_content.get_current_page_title",
        _("Set the page title."),
    ),
    "ogc:current_page_description": (
        "djangocms_meta_og.dynamic_content.get_current_page_description",
        _("Set the page description."),
    ),
    "ogc:filer_image_url": (
        "djangocms_meta_og.dynamic_content.get_filer_image_url",
        _("Set image URL by Filer ID. For example: ogc:filer_image_url(42)"),
    ),
}
```

### Edit form

In addition to administration, editing META values ​​is also available from the page menu.

![Page Meta OG menu](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og/-/raw/main/screenshots/meta-og-menu.png "Page Meta OG menu")

![Page Meta OG menu form](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og/-/raw/main/screenshots/meta-og-page-form.png "Page Meta OG menu form")


### Admininstration
 
You can enter any Meta values. These are entered in four levels - Namespace, Property, Content and PageMetaOg.
For this reason, a text form is set up for the META value, in which all these parts are combined in one edit in a text field.

![Page Meta OG form](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og/-/raw/main/screenshots/djangocms-pagemetaog-form.png "Page Meta OG form")

If you want to return to the default editing via select boxes, activate the switch in settings.py:

```python
META_OG_USE_DEFAULT_PAGE_FORM = True
```

![Page Meta OG default form](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og/-/raw/main/screenshots/djangocms-meta-og-default-admin-form.png "Page Meta OG default form")

#### Namespace
 
![Namespace list](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og/-/raw/main/screenshots/djangocms-namespace-list.png "Namespace list")
 
![Namespace form](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og/-/raw/main/screenshots/djangocms-namespace-form.png "Namespace form")
 
#### Property
 
![Property list](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og/-/raw/main/screenshots/djangocms-property-list.png "Property list")
 
![Property form](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og/-/raw/main/screenshots/djangocms-property-form.png "Property form")
 
#### Content
 
![Content list](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og/-/raw/main/screenshots/djangocms-content-list.png "Content list")
 
![Content form](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og/-/raw/main/screenshots/djangocms-content-form.png "Content form")

#### Page Meta OG
 
![Page Meta OG list](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og/-/raw/main/screenshots/djangocms-pagemetaog-list.png "Page Meta OG list")
 
![Page Meta OG form](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og/-/raw/main/screenshots/djangocms-pagemetaog-form.png "Page Meta OG form")


### License

BSD License
