from django.db.models.query import QuerySet
from django.http import HttpRequest

from .utils import get_page_meta


def meta(request: HttpRequest) -> dict[str, QuerySet]:
    """Add key django_meta_og into context."""

    if hasattr(request, "current_page") and hasattr(request.current_page, "pk"):
        page_meta = get_page_meta(request.current_page, request.LANGUAGE_CODE)
        if page_meta is not None:
            return {"django_meta_og": page_meta.meta.all()}
    return {}
