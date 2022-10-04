from attempts.viewsets import QuizInvitedAttemptViewset
from django.urls import include, path
from rest_framework_nested import routers

from .viewsets import QuizInvitedViewset, QuizOwnedInviteParticipantsViewset, QuizOwnedViewset

router = routers.SimpleRouter()
router.register("quizzes/owned", QuizOwnedViewset, "quizzes-owned")
router.register("quizzes/invited", QuizInvitedViewset, "quizzes-invited")

quizzes_owned_router = routers.NestedSimpleRouter(router, "quizzes/owned", lookup="owned")
quizzes_owned_router.register("invite", QuizOwnedInviteParticipantsViewset, basename="quizzes-owned-attempt")

quizzes_invited_router = routers.NestedSimpleRouter(router, "quizzes/invited", lookup="invited")
quizzes_invited_router.register("attempt", QuizInvitedAttemptViewset, basename="quizzes-invited-attempt")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(quizzes_owned_router.urls)),
    path("", include(quizzes_invited_router.urls)),
]
