from django.contrib import admin

from ..models import PageMetaOg
from .options import PageMetaOgAdmin

admin.site.register(PageMetaOg, PageMetaOgAdmin)
