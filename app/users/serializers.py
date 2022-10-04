from attempts.models import Attempt, AttemptAnswer
from django.contrib.auth import get_user_model
from quizzes.models import Answer, Quiz
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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
    finished = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "attempted",
            "finished",
        )

    def get_attempted(self, obj):
        return obj.attempts.filter(quiz=self.context["view"].kwargs.get("pk")).exists()

    def get_finished(self, obj):
        quiz = Quiz.objects.get(id=self.context["view"].kwargs.get("pk"))
        questions = quiz.questions.all()
        print(Answer.objects.filter(question__in=questions, is_correct=True))
        attempt = obj.attempts.filter(quiz=quiz)
        print(quiz.questions.all())
        print(attempt)
        return obj.attempts.filter(quiz=self.context["view"].kwargs.get("pk")).exists()


class QuizOwnedInviteParticipantsSerializer(serializers.Serializer):
    emails = serializers.ListField(child=serializers.EmailField())
