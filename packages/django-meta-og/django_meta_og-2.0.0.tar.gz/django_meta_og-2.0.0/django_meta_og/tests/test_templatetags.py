from django.test import RequestFactory, TestCase, override_settings

from django_meta_og.models import Content, Namespace, Property
from django_meta_og.templatetags.django_meta_og import django_meta_og_dynamic_content, django_meta_og_prefix


class DjangoMetaOGPrefixTest(TestCase):
    def setUp(self):
        ns, _ = Namespace.objects.get_or_create(prefix="og", uri="https://ogp.me/ns#")
        prop, _ = Property.objects.get_or_create(namespace=ns, name="type")
        Content.objects.create(property=prop, content="website")

    def test_prefix(self):
        self.assertEqual(django_meta_og_prefix(), "og: https://ogp.me/ns#")

    @override_settings(META_OG_PREFIX_IN_TEMLATES=(("article", "https://ogp.me/ns/article#"),))
    def test_prefix_in_template(self):
        self.assertEqual(django_meta_og_prefix(), "article: https://ogp.me/ns/article#\nog: https://ogp.me/ns#")

    def test_content(self):
        request = RequestFactory().request()
        value = django_meta_og_dynamic_content(request, "test")
        self.assertEqual(value, "test")

    @override_settings(
        PAGE_META_OG_DYNAMIC_CONTENT={"fnc:page_url": ("django_meta_og.dynamic_content.get_page_url", "Description.")}
    )
    def test_dynamic_content(self):
        request = RequestFactory().request()
        value = django_meta_og_dynamic_content({"request": request}, "fnc:page_url")
        self.assertEqual(value, "http%3A%2F%2Ftestserver%2F")

    @override_settings(
        PAGE_META_OG_DYNAMIC_CONTENT={"fnc:page_url": ("django_meta_og.dynamic_content.get_page_url", "Description.")}
    )
    def test_static_content(self):
        request = RequestFactory().request()
        value = django_meta_og_dynamic_content({"request": request}, "page_url")
        self.assertEqual(value, "page_url")

    @override_settings(
        PAGE_META_OG_DYNAMIC_CONTENT={"fnc:page_url": ("django_meta_og.dynamic_content.get_page_url", "Description.")}
    )
    def test_function_empty_parameter(self):
        request = RequestFactory().request()
        value = django_meta_og_dynamic_content({"request": request}, "fnc:page_url()")
        self.assertEqual(value, "http%3A%2F%2Ftestserver%2F")

    @override_settings(
        PAGE_META_OG_DYNAMIC_CONTENT={"fnc:page_url": ("django_meta_og.dynamic_content.get_page_url", "Description.")}
    )
    def test_function_some_parameter(self):
        request = RequestFactory().request()
        value = django_meta_og_dynamic_content({"request": request}, "fnc:page_url (42)")
        self.assertEqual(value, "http%3A%2F%2Ftestserver%2F")

    @override_settings(
        PAGE_META_OG_DYNAMIC_CONTENT={"fnc:page_url": ("django_meta_og.dynamic_content.get_page_url", "Description.")}
    )
    def test_function_more_parameters(self):
        request = RequestFactory().request()
        value = django_meta_og_dynamic_content({"request": request}, "fnc:page_url(1, 2, 3)")
        self.assertEqual(value, "http%3A%2F%2Ftestserver%2F")
