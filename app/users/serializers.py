from django.contrib.auth import get_user_model
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


class QuizOwnedInviteParticipantsSerializer(serializers.Serializer):
    emails = serializers.ListField(child=serializers.EmailField())
