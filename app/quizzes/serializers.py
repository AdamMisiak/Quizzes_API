from rest_framework import serializers

from .models import Answer, Question, Quiz


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "id",
            "content",
            "is_correct",
        )


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(required=True, many=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "content",
            "answers",
        )


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(required=True, many=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Quiz
        fields = (
            "id",
            "name",
            "owner",
            "questions",
        )
