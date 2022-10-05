from django.urls import include, path
from rest_framework_nested import routers

from .viewsets import QuizInvitationViewset

router = routers.SimpleRouter()
router.register("invitations", QuizInvitationViewset, "invitations")

urlpatterns = [
    path("", include(router.urls)),
]
