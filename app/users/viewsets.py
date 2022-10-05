from django.contrib.auth import get_user_model
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .enums import StatusChoices
from .models import QuizInvitation
from .serializers import QuizInvitationSerializer

User = get_user_model()


class QuizInvitationViewset(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = QuizInvitation.objects.all().select_related("owner", "invited", "quiz").order_by("-created")
    serializer_class = QuizInvitationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(invited=self.request.user, status=StatusChoices.SENT.value)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return QuizInvitationSerializer

    @action(methods=["POST"], detail=True)
    def accept(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.quiz.participants.add(request.user)
        obj.status = StatusChoices.ACCEPTED.value
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["POST"], detail=True)
    def reject(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.status = StatusChoices.REJECTED.value
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
