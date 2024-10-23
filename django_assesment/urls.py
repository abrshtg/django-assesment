from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularAPIView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("auth/", include("social_django.urls", namespace="social")),
    path("docs/", SpectacularSwaggerView.as_view(url_name="docs")),
    path("schema/", SpectacularAPIView.as_view(), name="docs"),
    # Optional UI:
]
