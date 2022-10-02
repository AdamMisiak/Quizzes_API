from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import Answer, Question, Quiz
from .serializers import QuizSerializer


class QuizViewset(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def create(self, request, *args, **kwargs):
        serializer = QuizSerializer(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid(raise_exception=True):
            questions = serializer.validated_data.pop("questions")
            if not questions:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            quiz = Quiz.objects.create(**serializer.validated_data)

            for question in questions:
                answers = question.pop("answers")
                if not answers:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                question_obj, created = Question.objects.get_or_create(quiz=quiz, **question)

                for answer in answers:
                    Answer.objects.get_or_create(question=question_obj, **answer)
            return Response(data=request.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
