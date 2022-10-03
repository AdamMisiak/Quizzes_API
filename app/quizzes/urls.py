from django.urls import include, path
from rest_framework_nested import routers

from .viewsets import QuizInvitedViewset, QuizOwnedViewset

router = routers.SimpleRouter()
router.register("quizzes/owned", QuizOwnedViewset, "quizzes-owned")
router.register("quizzes/invited", QuizInvitedViewset, "quizzes-invited")


urlpatterns = [
    path("", include(router.urls)),
]
