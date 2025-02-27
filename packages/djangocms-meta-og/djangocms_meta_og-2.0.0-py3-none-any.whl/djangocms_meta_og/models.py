from cms.models import Page
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_meta_og.models import Content


class PageMetaOg(models.Model):
    meta = models.ManyToManyField(Content)
    language = models.CharField(choices=settings.LANGUAGES, max_length=20)
    page = models.ForeignKey(
        Page,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text=_("A Meta without a page will be used for the entire site."),
    )

    class Meta:
        unique_together = [["language", "page"]]

    def __str__(self):
        if self.page is None:
            title = _("Entire website")
        else:
            title = str(self.page)
            if not title and hasattr(settings, "CMS_CONFIRM_VERSION4") and settings.CMS_CONFIRM_VERSION4:
                title = self.page.pagecontent_set(manager="admin_manager").last().title
        return str(title)
