from urllib.parse import quote

from django.http import HttpRequest


def get_page_url(request: HttpRequest, *args) -> str:
    """Get page url."""
    return quote(request.build_absolute_uri(), "&?")
