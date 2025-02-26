from unittest import skipIf

import django
from django.contrib import admin
from django.test import TestCase

from django_meta_og.models import Content, Namespace, Property


@skipIf(django.VERSION < (5, 0), "Skip Django < 5.0.")
class AdminTest(TestCase):
    def test_content(self):
        self.assertEqual(admin.site.get_model_admin(Content).ordering, ["property", "content"])

    def test_namespace(self):
        self.assertEqual(admin.site.get_model_admin(Namespace).ordering, ["prefix"])

    def test_property(self):
        self.assertEqual(admin.site.get_model_admin(Property).ordering, ["namespace", "name"])
