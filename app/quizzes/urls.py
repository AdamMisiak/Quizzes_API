from django.urls import include, path
from rest_framework_nested import routers

from .viewsets import QuizViewset

router = routers.SimpleRouter()
router.register("quizzes", QuizViewset, "quizzes")


urlpatterns = [
    path("", include(router.urls)),
]
