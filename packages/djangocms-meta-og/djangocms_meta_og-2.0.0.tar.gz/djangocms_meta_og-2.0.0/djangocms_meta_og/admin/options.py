from cms.utils import get_current_site
from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from django_meta_og.models import Content, Property

from .fields import PageField
from .forms import PageMetaOgForm, PageMetaOgTextareaForm


class PageMetaOgAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ["djangocms_meta_og/css/admin.css"],
        }
        js = ["djangocms_meta_og/js/admin.js"]

    form = PageMetaOgTextareaForm
    ordering = ["page", "language"]
    list_display = ["view_page", "language"]

    @admin.display(description=_("Page"))
    def view_page(self, obj):
        return str(obj)

    def get_site(self, request):
        site_id = request.session.get("cms_admin_site")
        if not site_id:
            return get_current_site()
        try:
            site = Site.objects._get_site_by_id(site_id)
        except Site.DoesNotExist:
            site = get_current_site()
        return site

    def get_form(self, request, obj=None, change=False, **kwargs):
        if hasattr(settings, "META_OG_USE_DEFAULT_PAGE_FORM") and settings.META_OG_USE_DEFAULT_PAGE_FORM:
            self.form = PageMetaOgForm
        form = super().get_form(request, obj, change, **kwargs)
        if "page" in form.base_fields:
            page = form.base_fields["page"]
            if hasattr(settings, "CMS_CONFIRM_VERSION4") and settings.CMS_CONFIRM_VERSION4:
                queryset = page.queryset.filter(node__site=self.get_site(request))
            else:
                queryset = page.queryset.filter(node__site=self.get_site(request), publisher_is_draft=True)
            form.base_fields["page"] = PageField(queryset=queryset, required=False, help_text=page.help_text)
        form.user = request.user
        return form

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context["meta_og_property"] = Property.objects.all().order_by("namespace", "name")
        extra_context["meta_og_content"] = Content.objects.all().order_by("property", "content")
        if hasattr(settings, "PAGE_META_OG_DYNAMIC_CONTENT"):
            extra_context["PAGE_META_OG_DYNAMIC_CONTENT"] = settings.PAGE_META_OG_DYNAMIC_CONTENT
        return super().changeform_view(request, object_id, form_url, extra_context)

    def render_change_form(self, request, context, add=False, change=False, form_url="", obj=None):
        if hasattr(settings, "META_OG_USE_DEFAULT_PAGE_FORM") and settings.META_OG_USE_DEFAULT_PAGE_FORM:
            self.add_form_template = self.change_form_template = "admin/change_form.html"
        return super().render_change_form(request, context, add, change, form_url, obj)
