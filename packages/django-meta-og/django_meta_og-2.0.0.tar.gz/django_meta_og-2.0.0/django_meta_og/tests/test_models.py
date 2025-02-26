from django.test import TestCase

from django_meta_og.models import Content, Namespace, Property


class TestNamespace(TestCase):
    def test_str(self):
        ns, _ = Namespace.objects.get_or_create(prefix="og", uri="https://ogp.me/ns#")
        self.assertEqual(str(ns), "og: https://ogp.me/ns#")


class TestProperty(TestCase):
    def setUp(self):
        self.ns, _ = Namespace.objects.get_or_create(prefix="og", uri="https://ogp.me/ns#")

    def test_str(self):
        prop, _ = Property.objects.get_or_create(namespace=self.ns, name="type")
        self.assertEqual(str(prop), "og:type")


class TestContent(TestCase):
    def setUp(self):
        self.ns, _ = Namespace.objects.get_or_create(prefix="og", uri="https://ogp.me/ns#")
        self.prop, _ = Property.objects.get_or_create(namespace=self.ns, name="type")

    def test_str(self):
        content = Content.objects.create(property=self.prop, content="website")
        self.assertEqual(str(content), "og:type website")
