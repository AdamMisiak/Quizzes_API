from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

# from django.utils.translation import ugettext_lazy as _

api_urlpatterns = [
    path("", include("quizzes.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    re_path("^api/(?P<version>(v1|v2))/", include((api_urlpatterns, "api"), namespace="api")),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
