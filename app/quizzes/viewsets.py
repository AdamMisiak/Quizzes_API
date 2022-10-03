from django_filters import rest_framework as filters
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .filters import QuizFilter
from .models import Answer, Question, Quiz
from .serializers import QuizCreateSerializer, QuizDetailsSerializer, QuizListSerializer


class QuizOwnedViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        Quiz.objects.all()
        .select_related("owner")
        .prefetch_related("participants", "questions", "questions__answers")
        .order_by("-created")
    )
    serializer_class = QuizListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = QuizFilter

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create"]:
            return QuizCreateSerializer
        elif self.action in ["list"]:
            return QuizListSerializer
        elif self.action in ["retrieve"]:
            return QuizDetailsSerializer

    def create(self, request, *args, **kwargs):
        serializer = QuizCreateSerializer(data=request.data, context=self.get_serializer_context())
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


class QuizInvitedViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        Quiz.objects.all()
        .select_related("owner")
        .prefetch_related("participants", "questions", "questions__answers")
        .order_by("-created")
    )
    serializer_class = QuizListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = QuizFilter

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)
