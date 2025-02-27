from cms.api import create_page
from cms.test_utils.testcases import CMSTestCase
from django.conf import settings
from django_meta_og.models import Content, Namespace, Property

from djangocms_meta_og.models import PageMetaOg


class TestPageMetaOg(CMSTestCase):
    def setUp(self):
        ns, _ = Namespace.objects.get_or_create(prefix="og", uri="https://ogp.me/ns#")
        prop, _ = Property.objects.get_or_create(namespace=ns, name="type")
        self.content = Content.objects.create(property=prop, content="website")

    def test_entire_site(self):
        meta = PageMetaOg.objects.create(language=settings.LANGUAGE_CODE)
        meta.meta.add(self.content)
        self.assertEqual(str(meta), "Entire website")

    def test_page(self):
        page = create_page("home", "page.html", settings.LANGUAGE_CODE)
        meta = PageMetaOg.objects.create(language=settings.LANGUAGE_CODE, page=page)
        meta.meta.add(self.content)
        self.assertEqual(str(meta), "home")
