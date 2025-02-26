from django.test import RequestFactory, TestCase

from django_meta_og.context_processors import meta
from django_meta_og.models import Content, Namespace, Property


class MetaTest(TestCase):
    def test(self):
        ns, _ = Namespace.objects.get_or_create(prefix="og", uri="https://ogp.me/ns#")
        prop, _ = Property.objects.get_or_create(namespace=ns, name="type")
        Content.objects.create(property=prop, content="website")
        context = meta(RequestFactory().request())
        self.assertEqual(list(context.keys()), ["django_meta_og"])
        self.assertQuerySetEqual(context["django_meta_og"], Content.objects.all())
