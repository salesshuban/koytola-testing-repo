from django.db import models

from ..core.db.fields import SanitizedJSONField
from ..core.models import (
    ModelWithMetadata,
    PublishableModel,
    PublishedQuerySet
)
from ..core.permissions import PagePermissions
from ..core.utils.editorjs import clean_editor_js
from ..core.utils.translations import TranslationProxy
from ..seo.models import SeoModel, SeoModelTranslation


class PagePublishedQuerySet(PublishedQuerySet):
    @staticmethod
    def user_has_access_to_all(user):
        return user.is_active and user.has_perm(PagePermissions.MANAGE_PAGES)


class Page(ModelWithMetadata, SeoModel, PublishableModel):
    slug = models.SlugField(unique=True, max_length=255)
    title = models.CharField(max_length=250)
    summary = models.CharField(max_length=320)
    page_type = models.ForeignKey(
        "PageType", related_name="pages", on_delete=models.CASCADE
    )
    content = SanitizedJSONField(blank=True, default=dict, sanitizer=clean_editor_js)
    content_plaintext = models.TextField(blank=True, default="")

    objects = PagePublishedQuerySet.as_manager()
    translated = TranslationProxy()

    class Meta:
        ordering = ["slug"]
        permissions = [(PagePermissions.MANAGE_PAGES.codename, "Manage pages.")]

    def __str__(self):
        return self.title


class PageTranslation(SeoModelTranslation):
    language_code = models.CharField(max_length=10)
    page = models.ForeignKey(
        Page, related_name="translations", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, blank=True)
    summary = models.CharField(max_length=320, blank=True)
    content = SanitizedJSONField(blank=True, default=dict, sanitizer=clean_editor_js)
    content_plaintext = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["language_code", "page", "pk"]
        unique_together = [("language_code", "page")]

    def __repr__(self):
        class_ = type(self)
        return "%s(pk=%r, title=%r, page_pk=%r)" % (
            class_.__name__,
            self.pk,
            self.title,
            self.page_id,
        )

    def __str__(self):
        return self.title


class PageType(ModelWithMetadata):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)

    class Meta:
        ordering = ["slug"]
        permissions = (
            (
                PagePermissions.MANAGE_PAGE_TYPES.codename,
                "Manage page types.",
            ),
        )
