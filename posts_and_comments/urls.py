from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("captcha/", include("captcha.urls")),
    path("", include("blog.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]
