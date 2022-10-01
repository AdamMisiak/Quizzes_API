from django.conf import settings
from rest_framework import serializers

from .models import Quiz


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = (
            "id",
            "name",
        )
