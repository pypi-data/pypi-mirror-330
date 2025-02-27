from typing import Any

from django import template
from django.conf import settings

from djangocms_meta_og.utils import get_page_meta

register = template.Library()


@register.simple_tag(takes_context=True)
def djangocms_meta_og_prefix(context: dict[str, Any]) -> str:
    prefixes = set()
    if hasattr(settings, "META_OG_PREFIX_IN_TEMLATES"):
        prefixes.update(settings.META_OG_PREFIX_IN_TEMLATES)
    request = context["request"]
    current_page = context.get("current_page", getattr(request, "current_page", None))
    if hasattr(current_page, "pk"):
        page_meta = get_page_meta(current_page, request.LANGUAGE_CODE)
        if page_meta is not None:
            for meta in page_meta.meta.all():
                prefixes.add((meta.property.namespace.prefix, meta.property.namespace.uri))
    return "\n".join({f"{prefix}: {uri}" for prefix, uri in prefixes})
