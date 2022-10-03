from attempts.models import Attempt, AttemptAnswer
from rest_framework import serializers
from users.serializers import UserSimpleSerializer
from utils.serializers import CurrentUrlObject

from .models import Answer, Question, Quiz


class AnswerIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id",)


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


class QuestionIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id",)


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
            "user",
            "answers",
        )


class QuizDetailsSerializer(QuizListSerializer):
    attempts = AttemptListSerializer(many=True)

    class Meta(QuizListSerializer.Meta):
        fields = (*QuizListSerializer.Meta.fields, "attempts")


# {
#     "answers": [
#         {
#             "question": 2,
#             "answer": 4
#         }
#     ]
# }
