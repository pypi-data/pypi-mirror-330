from typing import Optional

from cms.models import Page

from .models import PageMetaOg


def get_page_meta(current_page: Page, language: str) -> Optional[PageMetaOg]:
    """Get meta OG for current page."""
    meta: Optional[PageMetaOg] = None
    # Meta for draft page.
    try:
        meta = PageMetaOg.objects.get(page=current_page, language=language)
    except PageMetaOg.DoesNotExist:
        pass
    # Meta for public page.
    if meta is None and hasattr(current_page, "publisher_public"):
        try:
            meta = PageMetaOg.objects.get(page=current_page.publisher_public, language=language)
        except PageMetaOg.DoesNotExist:
            pass
    # Global Meta with no page.
    if meta is None:
        try:
            meta = PageMetaOg.objects.get(page__isnull=True, language=language)
        except PageMetaOg.DoesNotExist:
            pass
    return meta
