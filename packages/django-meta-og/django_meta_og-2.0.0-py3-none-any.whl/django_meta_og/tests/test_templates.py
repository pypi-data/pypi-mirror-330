from django.test import TestCase, override_settings

from django_meta_og.models import Content, Namespace, Property


@override_settings(ROOT_URLCONF="django_meta_og.tests.urls")
class TemplateViewTest(TestCase):
    def test(self):
        ns, _ = Namespace.objects.get_or_create(prefix="og", uri="https://ogp.me/ns#")
        prop_type, _ = Property.objects.get_or_create(namespace=ns, name="type")
        prop_title, _ = Property.objects.get_or_create(namespace=ns, name="title")
        Content.objects.create(property=prop_type, content="website")
        Content.objects.create(property=prop_title, content="The Title")

        response = self.client.get("/page-headers/")
        self.assertContains(
            response,
            """
            <meta property="og:type" content="website">
            <meta property="og:title" content="The Title">""",
            html=True,
        )
