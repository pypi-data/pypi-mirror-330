import re

from django import template
from django.conf import settings

from django_meta_og.models import Content

from ..utils import get_or_create_fnc

register = template.Library()


@register.simple_tag()
def django_meta_og_prefix():
    prefixes = set()
    if hasattr(settings, "META_OG_PREFIX_IN_TEMLATES"):
        prefixes.update(settings.META_OG_PREFIX_IN_TEMLATES)
    for meta in Content.objects.all():
        prefixes.add((meta.property.namespace.prefix, meta.property.namespace.uri))
    return "\n".join([f"{prefix}: {uri}" for prefix, uri in sorted(prefixes)])


@register.simple_tag(takes_context=True)
def django_meta_og_dynamic_content(context: dict, value: str) -> str:
    if hasattr(settings, "PAGE_META_OG_DYNAMIC_CONTENT"):
        fnc_name, params = value, []
        match = re.match(r"(?P<name>.+)\s*\((?P<params>.*)\)", value)
        if match:
            fnc_name = match.group("name").strip()
            for item in re.split(r",\s*", match.group("params").strip()):
                params.append(item.strip())
        path_and_description = settings.PAGE_META_OG_DYNAMIC_CONTENT.get(fnc_name)
        if path_and_description:
            return get_or_create_fnc(path_and_description[0])(context["request"], *params)
    return value
