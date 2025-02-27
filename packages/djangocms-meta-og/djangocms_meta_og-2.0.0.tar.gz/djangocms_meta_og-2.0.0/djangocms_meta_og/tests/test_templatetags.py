from cms.api import create_page
from cms.test_utils.testcases import CMSTestCase
from django.conf import settings
from django.test import RequestFactory, override_settings
from django_meta_og.models import Content, Namespace, Property
from django_meta_og.templatetags.django_meta_og import django_meta_og_dynamic_content

from djangocms_meta_og.models import PageMetaOg
from djangocms_meta_og.templatetags.djangocms_meta_og import djangocms_meta_og_prefix


class DjangoMetaOGPrefixTest(CMSTestCase):
    def setUp(self):
        ns, _ = Namespace.objects.get_or_create(prefix="og", uri="https://ogp.me/ns#")
        prop, _ = Property.objects.get_or_create(namespace=ns, name="type")
        self.content = Content.objects.create(property=prop, content="website")
        self.page = create_page("home", "page.html", settings.LANGUAGE_CODE)

    def test(self):
        page_meta = PageMetaOg.objects.create(language=settings.LANGUAGE_CODE, page=self.page)
        page_meta.meta.add(self.content)
        request = RequestFactory().request()
        request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        context = {"request": request, "current_page": self.page}
        self.assertEqual(djangocms_meta_og_prefix(context), "og: https://ogp.me/ns#")

    def test_no_current_page(self):
        request = RequestFactory().request()
        request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        context = {"request": request}
        self.assertEqual(djangocms_meta_og_prefix(context), "")

    def test_no_page_meta(self):
        request = RequestFactory().request()
        request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        context = {"request": request, "current_page": self.page}
        self.assertEqual(djangocms_meta_og_prefix(context), "")


class DynamicContentTest(CMSTestCase):
    def setUp(self):
        self.page = create_page("home", "page.html", settings.LANGUAGE_CODE)

    @override_settings(
        PAGE_META_OG_DYNAMIC_CONTENT={"fnc:page_url": ("djangocms_meta_og.dynamic_content.get_current_page_url", "")},
        ROOT_URLCONF="cms.urls",
    )
    def test_get_current_page_url(self):
        request = RequestFactory().request()
        request.current_page = self.page
        value = django_meta_og_dynamic_content({"request": request}, "fnc:page_url")
        self.assertEqual(value, "http%3A%2F%2Ftestserver%2Fhome%2F")

    @override_settings(
        PAGE_META_OG_DYNAMIC_CONTENT={"fc:pg_title": ("djangocms_meta_og.dynamic_content.get_current_page_title", "")},
        ROOT_URLCONF="cms.urls",
    )
    def test_get_page_title(self):
        request = RequestFactory().request()
        request.current_page = self.page
        value = django_meta_og_dynamic_content({"request": request}, "fc:pg_title")
        self.assertEqual(value, "home")

    @override_settings(
        PAGE_META_OG_DYNAMIC_CONTENT={
            "fc:pg_descr": ("djangocms_meta_og.dynamic_content.get_current_page_description", "Description")
        },
        ROOT_URLCONF="cms.urls",
    )
    def test_get_page_description(self):
        page_content = self.page.get_content_obj()
        page_content.meta_description = "The page description."
        page_content.save()
        request = RequestFactory().request()
        request.current_page = self.page
        value = django_meta_og_dynamic_content({"request": request}, "fc:pg_descr")
        self.assertEqual(value, "The page description.")

    @override_settings(
        PAGE_META_OG_DYNAMIC_CONTENT={"fnc:image_url": ("djangocms_meta_og.dynamic_content.get_filer_image_url", "")},
    )
    def test_get_filer_image_url_no_filer(self):
        request = RequestFactory().request()
        request.current_page = self.page
        value = django_meta_og_dynamic_content({"request": request}, "fnc:image_url")
        self.assertEqual(value, "")

    @override_settings(
        PAGE_META_OG_DYNAMIC_CONTENT={"fnc:image_url": ("djangocms_meta_og.dynamic_content.get_filer_image_url", "")},
    )
    def test_get_filer_image_url_no_args(self):
        request = RequestFactory().request()
        request.current_page = self.page
        value = django_meta_og_dynamic_content({"request": request}, "fnc:image_url()")
        self.assertEqual(value, "")

    @override_settings(
        PAGE_META_OG_DYNAMIC_CONTENT={"fnc:image_url": ("djangocms_meta_og.dynamic_content.get_filer_image_url", "")},
    )
    def test_get_filer_image_url_no_int(self):
        request = RequestFactory().request()
        request.current_page = self.page
        value = django_meta_og_dynamic_content({"request": request}, "fnc:image_url(foo)")
        self.assertEqual(value, "")


# @modify_settings(INSTALLED_APPS={"append": ["filer", "easy_thumbnails"]})
# class DynamicContentImageTest(CMSTestCase):
#     def setUp(self):
#         self.page = create_page("home", "page.html", settings.LANGUAGE_CODE)

#     @override_settings(
#         PAGE_META_OG_DYNAMIC_CONTENT={"fnc:image_url": ("djangocms_meta_og.dynamic_content.get_filer_image_url", "")},
#     )
#     def test_get_filer_image_url_not_found(self):
#         request = RequestFactory().request()
#         request.current_page = self.page
#         value = django_meta_og_dynamic_content({"request": request}, "fnc:image_url(42)")
#         self.assertEqual(value, "")
