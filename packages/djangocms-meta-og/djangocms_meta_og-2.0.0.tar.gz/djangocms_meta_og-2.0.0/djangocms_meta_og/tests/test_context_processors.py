from cms.api import create_page
from cms.test_utils.testcases import CMSTestCase
from django.conf import settings
from django.test import RequestFactory
from django_meta_og.models import Content, Namespace, Property

from djangocms_meta_og.context_processors import meta
from djangocms_meta_og.models import PageMetaOg


class MetaTest(CMSTestCase):
    def setUp(self):
        ns, _ = Namespace.objects.get_or_create(prefix="og", uri="https://ogp.me/ns#")
        prop, _ = Property.objects.get_or_create(namespace=ns, name="type")
        self.content = Content.objects.create(property=prop, content="website")
        self.page = create_page("home", "page.html", settings.LANGUAGE_CODE)

    def test(self):
        page_meta = PageMetaOg.objects.create(language=settings.LANGUAGE_CODE, page=self.page)
        page_meta.meta.add(self.content)

        request = RequestFactory().request()
        request.current_page = self.page
        request.LANGUAGE_CODE = settings.LANGUAGE_CODE

        context = meta(request)

        self.assertEqual(list(context.keys()), ["django_meta_og"])
        self.assertQuerySetEqual(context["django_meta_og"], page_meta.meta.all())

    def test_no_page(self):
        page_meta = PageMetaOg.objects.create(language=settings.LANGUAGE_CODE, page=self.page)
        page_meta.meta.add(self.content)

        request = RequestFactory().request()
        context = meta(request)
        self.assertEqual(list(context.keys()), [])

    def test_no_meta(self):
        request = RequestFactory().request()
        request.current_page = self.page
        request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        context = meta(request)
        self.assertEqual(list(context.keys()), [])
