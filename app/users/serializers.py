from attempts.models import Attempt, AttemptAnswer
from django.contrib.auth import get_user_model
from quizzes.models import Answer, Quiz
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import QuizInvitation

User = get_user_model()


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
        )


class UserWithStatsSerializer(serializers.ModelSerializer):
    attempted = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "attempted",
        )

    def get_attempted(self, obj):
        return obj.attempts.filter(quiz=self.context["view"].kwargs.get("pk")).exists()


class QuizOwnedInviteParticipantsSerializer(serializers.Serializer):
    emails = serializers.ListField(child=serializers.EmailField())


class QuizSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = (
            "id",
            "name",
        )


class QuizInvitationSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer()
    quiz = QuizSimpleSerializer()

    class Meta:
        model = QuizInvitation
        fields = (
            "id",
            "owner",
            "quiz",
            "status",
            "created",
        )
