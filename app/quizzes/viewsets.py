from rest_framework import generics, mixins, permissions, status, viewsets

from .models import Quiz
from .serializers import QuizSerializer


class QuizViewset(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Quiz.objects.all()

    serializer_class = QuizSerializer
