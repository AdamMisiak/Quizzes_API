from django_filters import rest_framework as filters
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .filters import QuizFilter
from .models import Answer, Question, Quiz
from .serializers import QuizSerializer


class QuizViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    # NOTE: change to quizzes/owned and quizzes/invited? or
    queryset = (
        Quiz.objects.all()
        .select_related("owner")
        .prefetch_related("participants", "questions", "questions__answers")
        .order_by("-created")
    )
    serializer_class = QuizSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = QuizFilter

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

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
