from django.conf import settings
from django.contrib import admin

from .models import Content, Namespace, Property


@admin.register(Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    ordering = ["prefix"]


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    ordering = ["namespace", "name"]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    ordering = ["property", "content"]

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        if hasattr(settings, "PAGE_META_OG_DYNAMIC_CONTENT"):
            if extra_context is None:
                extra_context = {}
            extra_context["PAGE_META_OG_DYNAMIC_CONTENT"] = settings.PAGE_META_OG_DYNAMIC_CONTENT
        return super().changeform_view(request, object_id, form_url, extra_context)
