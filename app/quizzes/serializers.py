from attempts.models import Attempt, AttemptAnswer
from rest_framework import serializers
from users.serializers import UserSimpleSerializer, UserWithStatsSerializer
from utils.serializers import CurrentUrlObject

from .models import Answer, Question, Quiz


class AnswerIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id",)


class AnswerSimpleSerializer(AnswerIdSerializer):
    class Meta(AnswerIdSerializer.Meta):
        fields = (*AnswerIdSerializer.Meta.fields, "content")


class AnswerSerializer(AnswerSimpleSerializer):
    class Meta(AnswerSimpleSerializer.Meta):
        fields = (*AnswerSimpleSerializer.Meta.fields, "is_correct")


class QuestionIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id",)


class QuestionSimpleSerializer(QuestionIdSerializer):
    class Meta(QuestionIdSerializer.Meta):
        fields = (*QuestionIdSerializer.Meta.fields, "content")


class QuestionSerializer(QuestionSimpleSerializer):
    answers = AnswerSerializer(required=True, many=True)

    class Meta(QuestionSimpleSerializer.Meta):
        fields = (*QuestionSimpleSerializer.Meta.fields, "answers")


class QuizCreateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(required=True, many=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Quiz
        fields = (
            "name",
            "owner",
            "questions",
        )


class QuizListSerializer(QuizCreateSerializer):
    owner = UserSimpleSerializer()
    participants = UserSimpleSerializer(many=True)

    class Meta(QuizCreateSerializer.Meta):
        fields = ("id", *QuizCreateSerializer.Meta.fields, "participants")


class AttemptAnswerCreateSerializer(serializers.ModelSerializer):
    # TODO here can be implemented custom field SerializerMethodField with correct filter :)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answer = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all())

    class Meta:
        model = AttemptAnswer
        fields = (
            "question",
            "answer",
        )


class AttemptAnswerListSerializer(serializers.ModelSerializer):
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


class AttemptCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    quiz = serializers.HiddenField(default=CurrentUrlObject(Quiz, "invited_pk"))
    answers = AttemptAnswerCreateSerializer(many=True)

    class Meta:
        model = Attempt
        fields = (
            "user",
            "quiz",
            "answers",
        )


class AttemptListSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    answers = AttemptAnswerListSerializer(many=True)

    class Meta:
        model = Attempt
        fields = (
            "id",
            "is_finished",
            "is_successful",
            "user",
            "answers",
        )


class QuizDetailsSerializer(QuizListSerializer):
    participants = UserWithStatsSerializer(many=True)
    attempts = AttemptListSerializer(many=True)

    class Meta(QuizListSerializer.Meta):
        fields = (*QuizListSerializer.Meta.fields, "attempts")
