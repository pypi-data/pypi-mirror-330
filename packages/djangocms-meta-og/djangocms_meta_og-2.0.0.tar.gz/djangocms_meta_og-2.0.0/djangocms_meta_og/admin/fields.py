from django.conf import settings
from django.forms import ModelChoiceField


class PageField(ModelChoiceField):
    def label_from_instance(self, page) -> str:
        title = str(page)
        if not title and hasattr(settings, "CMS_CONFIRM_VERSION4") and settings.CMS_CONFIRM_VERSION4:
            title = str(page.pagecontent_set(manager="admin_manager").last().title)
        return title
