from quizzes.serializers import AttemptCreateSerializer
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import Attempt, AttemptAnswer


class QuizInvitedAttemptViewset(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AttemptCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = AttemptCreateSerializer(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid(raise_exception=True):
            answer_attempts = serializer.validated_data.pop("answers")
            if not answer_attempts:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            attempt = Attempt.objects.create(**serializer.validated_data)

            for answer_attempt in answer_attempts:
                AttemptAnswer.objects.create(
                    attempt=attempt, is_correct=answer_attempt.get("answer").is_correct, **answer_attempt
                )
            return Response(data=request.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
