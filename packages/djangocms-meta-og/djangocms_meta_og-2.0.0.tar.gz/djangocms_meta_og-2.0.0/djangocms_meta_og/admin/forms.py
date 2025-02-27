import re
from typing import Any, Union

from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelform_factory
from django.utils.translation import gettext_lazy as _
from django_meta_og.models import Content, Namespace, Property

from ..models import PageMetaOg


class PageMetaOgForm(forms.ModelForm):
    class Meta:
        model = PageMetaOg
        exclude = []

    def clean_page(self):
        page = self.cleaned_data["page"]
        if page is None:
            query = PageMetaOg.objects.filter(page__isnull=True)
            if self.instance.pk is not None:
                query &= query.exclude(pk=self.instance.pk)
            if query.exists():
                raise ValidationError(_("Page meta OG for entire site with this language already exists."))
        return page


class PageMetaOgTextareaForm(PageMetaOgForm):
    meta = forms.CharField(widget=forms.Textarea)

    def get_initial_for_field(self, field: forms.Field, field_name: str) -> Any:
        initial = super().get_initial_for_field(field, field_name)
        if field_name == "meta" and initial is not None:
            initial = "\n".join([f"{meta.property} {meta.content}" for meta in initial])
        return initial

    def clean_meta(self):
        meta = []
        for ns, name, text in self._parse_data():
            property = self._clean_property(ns, name)
            content = self._clean_content(ns, name, property, text)
            meta.append((property, content))
        return meta

    def _parse_data(self):
        """Parse data from text."""
        data = []
        for line in re.split(r"[\r\n]+", self.cleaned_data["meta"]):
            stripped_line = line.strip()
            if stripped_line == "":
                continue
            match = re.match(r"(?P<prefix>\w+?):(?P<name>\S+)\s+(?P<content>.+)", stripped_line)
            if not match:
                raise ValidationError(_("Invalid line") + f': "{line}"', code="invalid")
            prefix = match.group("prefix")
            try:
                ns = Namespace.objects.get(prefix=prefix)
            except Namespace.DoesNotExist:
                raise ValidationError(
                    _("Unknown prefix") + f': "{prefix}" ' + _("at line") + f' "{line}"', code="unknown_prefix"
                ) from None
            data.append((ns, match.group("name"), match.group("content")))
        return data

    def _clean_property(self, ns: Namespace, name: str) -> Union[Property, forms.ModelForm]:
        try:
            property = Property.objects.get(namespace=ns, name=name)
        except Property.DoesNotExist:
            if not self.user.has_perm("django_meta_og.add_property"):
                raise ValidationError(
                    _("You do not have permission to create meta name") + f' "{ns.prefix}:{name}"',
                    code="no_permission",
                ) from None
            PropertyForm = modelform_factory(Property, exclude=[])
            form = PropertyForm({"namespace": ns, "name": name})
            if not form.is_valid():
                raise ValidationError(
                    _("Invalid property") + f': "{ns.prefix}:{name}" ' + form.errors.as_text(), code="invalid"
                ) from None
            property = form
        return property

    def _clean_content(
        self, ns: Namespace, name: str, property: Union[Property, forms.ModelForm], text: str
    ) -> Union[Content, str]:
        if not isinstance(property, Property):
            property = Property.objects.first()
            if property is None:
                raise ValidationError("Meta OG Property missing.")
        try:
            content = Content.objects.get(property=property, content=text)
        except Content.DoesNotExist:
            if not self.user.has_perm("django_meta_og.add_content"):
                raise ValidationError(
                    _("You do not have permission to create meta content") + f' "{ns.prefix}:{name} {text}"',
                    code="no_permission",
                ) from None
            ContentForm = modelform_factory(Content, exclude=[])
            form = ContentForm({"property": property, "content": text})
            if not form.is_valid():
                raise ValidationError(
                    _("Invalid content") + f': "{ns.prefix}:{name}" ' + form.errors.as_text(), code="invalid"
                ) from None
            content = text
        return content

    def _save_m2m(self):
        cleaned_data = []
        meta_id = []
        for property, content in self.cleaned_data["meta"]:
            if isinstance(content, Content):
                cleaned_data.append(content)
            else:
                if isinstance(property, forms.ModelForm):
                    property = property.save()
                content, _ = Content.objects.get_or_create(property=property, content=content)
                cleaned_data.append(content)
            meta_id.append(content.pk)
        self.cleaned_data["meta"] = cleaned_data
        if self.user.has_perm("django_meta_og.delete_content"):
            for removed in self.instance.meta.exclude(pk__in=meta_id):
                if not removed.pagemetaog_set.exclude(page=self.instance.page).exists():
                    removed.delete()
        return super()._save_m2m()
