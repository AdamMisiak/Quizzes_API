from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

api_urlpatterns = [
    path("", include("quizzes.urls")),
    path("", include("users.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    re_path("^api/(?P<version>(v1|v2))/", include((api_urlpatterns, "api"), namespace="api")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework import permissions

    schema_view = get_schema_view(
        openapi.Info(
            title="Quiz API",
            default_version="v1",
            description="Quiz API Documentation",
        ),
        validators=["flex"],
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns.extend(
        [
            path(
                "swagger/",
                schema_view.with_ui("swagger", cache_timeout=0),
                name="schema-swagger-ui",
            ),
            path(
                "doc/",
                schema_view.with_ui("redoc", cache_timeout=0),
                name="schema-redoc",
            ),
        ]
    )
