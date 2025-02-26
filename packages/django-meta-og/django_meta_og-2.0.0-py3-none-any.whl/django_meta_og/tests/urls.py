from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("page-headers/", TemplateView.as_view(template_name="django_meta_og/header_meta.html")),
    path("test_admin/admin/", admin.site.urls),
]
