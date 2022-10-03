from attempts.viewsets import QuizInvitedAttemptViewset
from django.urls import include, path
from rest_framework_nested import routers

from .viewsets import QuizInvitedViewset, QuizOwnedViewset

router = routers.SimpleRouter()
router.register("quizzes/owned", QuizOwnedViewset, "quizzes-owned")
router.register("quizzes/invited", QuizInvitedViewset, "quizzes-invited")

quizzes_invited_router = routers.NestedSimpleRouter(router, "quizzes/invited", lookup="invited")
quizzes_invited_router.register("attempt", QuizInvitedAttemptViewset, basename="quizzes-invited-attempt")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(quizzes_invited_router.urls)),
]
