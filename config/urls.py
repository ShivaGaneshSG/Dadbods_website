"""
Root URL configuration for DadBods Coaching Platform.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    # Admin Portal
    path("admin/", admin.site.urls),

    # Applications System (Apply, Success, Staff Dashboard)
    path("", include("applications.urls", namespace="applications")),

    # Public Core Website (Home, About, Coaches, Coaching, Transformations)
    path("", include("core.urls", namespace="core")),

    # Dedicated DadBods image directory serving
    re_path(
        r"^images/(?P<path>.*)$",
        serve,
        {"document_root": settings.DADBODS_IMAGE_ROOT},
        name="dadbods_images",
    ),
]

# Static & Media serving during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
