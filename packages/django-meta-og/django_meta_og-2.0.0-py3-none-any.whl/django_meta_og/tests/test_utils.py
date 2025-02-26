from django.test import RequestFactory, SimpleTestCase

from django_meta_og.utils import get_or_create_fnc


class UtilsTest(SimpleTestCase):
    def test(self):
        fnc = get_or_create_fnc("django_meta_og.dynamic_content.get_page_url")
        request = RequestFactory().request()
        response = fnc(request)
        self.assertEqual(response, "http%3A%2F%2Ftestserver%2F")
