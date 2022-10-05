from quizzes.serializers import AttemptCreateSerializer
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from .models import Attempt, AttemptAnswer


class QuizInvitedAttemptViewset(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AttemptCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # NOTE check what will happen when wrong id will be provided - from different quiz
    def create(self, request, *args, **kwargs):
        serializer = AttemptCreateSerializer(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid(raise_exception=True):
            answer_attempts = serializer.validated_data.pop("answers")
            if not answer_attempts:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            attempt = Attempt.objects.create(**serializer.validated_data)
            attempt_answer_objects = []
            correct_attempt_answer_objects = []

            for answer_attempt in answer_attempts:
                attempt_answer_object = AttemptAnswer.objects.create(
                    attempt=attempt, is_correct=answer_attempt.get("answer").is_correct, **answer_attempt
                )
                attempt_answer_objects.append(attempt_answer_object)
                if attempt_answer_object.is_correct:
                    correct_attempt_answer_objects.append(attempt_answer_object)

            quiz = serializer.validated_data.get("quiz")
            quiz_questions = quiz.questions.all()
            quiz_questions_answered = quiz.questions.filter(attempts__in=attempt_answer_objects)
            if set(quiz_questions) == set(quiz_questions_answered):
                attempt.is_finished = True
                quiz_questions_correct_answered = quiz.questions.filter(attempts__in=correct_attempt_answer_objects)
                if set(quiz_questions) == set(quiz_questions_correct_answered):
                    attempt.is_successful = True
                    # NOTE send email to participant that he succeed quiz
                attempt.save()

            return Response(data=request.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
