from cms.api import get_page_draft
from cms.cms_toolbars import PAGE_MENU_SECOND_BREAK
from cms.toolbar.items import Break
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.permissions import has_page_permission
from django.conf import settings
from django.urls import NoReverseMatch, reverse

from .models import PageMetaOg

try:
    from cms.utils import get_cms_setting
except ImportError:
    from cms.utils.conf import get_cms_setting


META_OG_MENU_TITLE = "Page Meta"
META_OG_ITEM_TITLE = "Open Graph"


@toolbar_pool.register
class PageToolbarMeta(CMSToolbar):
    def populate(self):  # noqa: C901
        if hasattr(settings, "CMS_CONFIRM_VERSION4") and settings.CMS_CONFIRM_VERSION4:
            self.page = self.request.current_page
        else:
            self.page = get_page_draft(self.request.current_page)
        if not self.page:
            return
        if self.page.is_page_type:
            return

        if get_cms_setting("PERMISSION"):
            has_global_current_page_change_permission = has_page_permission(
                self.request.user, self.request.current_page, "change"
            )
        else:
            has_global_current_page_change_permission = False

        permission = self.request.current_page.has_change_permission(self.request.user)
        can_change = self.request.current_page and permission
        if has_global_current_page_change_permission or can_change:
            not_edit_mode = not self.toolbar.edit_mode_active

            current_page_menu = self.toolbar.get_or_create_menu("page")
            super_item = current_page_menu.find_first(Break, identifier=PAGE_MENU_SECOND_BREAK)
            if super_item:
                super_item = super_item + 1
            meta_menu = current_page_menu.get_or_create_menu(
                "metaog", META_OG_MENU_TITLE, position=super_item, disabled=not_edit_mode
            )
            user_has_perm = False
            try:
                page_meta_og = PageMetaOg.objects.get(page=self.page)
                user_has_perm = self.request.user.has_perm("djangocms_meta_og.view_pagemetaog")
            except PageMetaOg.DoesNotExist:
                page_meta_og = None
            try:
                if page_meta_og:
                    url = reverse("admin:djangocms_meta_og_pagemetaog_change", args=(page_meta_og.pk,))
                    if self.request.user.has_perm("djangocms_meta_og.change_pagemetaog"):
                        user_has_perm = True
                else:
                    path = reverse("admin:djangocms_meta_og_pagemetaog_add")
                    url = f"{path}?page={self.page.pk}&language={self.request.LANGUAGE_CODE}"
                    if self.request.user.has_perm("djangocms_meta_og.add_pagemetaog"):
                        user_has_perm = True
            except NoReverseMatch:
                pass
            else:
                if not user_has_perm:
                    not_edit_mode = True
                meta_menu.add_modal_item(META_OG_ITEM_TITLE, url=url, disabled=not_edit_mode, position=0)
