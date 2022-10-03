from attempts.models import Attempt, AttemptAnswer
from rest_framework import serializers
from users.serializers import UserSimpleSerializer

from .models import Answer, Question, Quiz


class AnswerSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "id",
            "content",
        )


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "id",
            "content",
            "is_correct",
        )


# NOTE make simple serializers parents of full serializers
class QuestionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "id",
            "content",
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


class QuizCreateSerializer(serializers.ModelSerializer):
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


class QuizListSerializer(QuizCreateSerializer):
    owner = UserSimpleSerializer()
    participants = UserSimpleSerializer(many=True)

    class Meta(QuizCreateSerializer.Meta):
        fields = (*QuizCreateSerializer.Meta.fields, "participants")


class AttemptAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSimpleSerializer()
    answer = AnswerSimpleSerializer()

    class Meta:
        model = AttemptAnswer
        fields = (
            "id",
            "question",
            "answer",
            "created",
        )


class AttemptSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    answers = AttemptAnswerSerializer(many=True)

    class Meta:
        model = Attempt
        fields = (
            "id",
            "user",
            "answers",
        )


class QuizDetailsSerializer(QuizListSerializer):
    attempts = AttemptSerializer(many=True)

    class Meta(QuizListSerializer.Meta):
        fields = (*QuizListSerializer.Meta.fields, "attempts")
