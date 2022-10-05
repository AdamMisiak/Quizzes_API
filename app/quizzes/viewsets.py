from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response
from users.enums import StatusChoices
from users.models import QuizInvitation
from users.serializers import QuizOwnedInviteParticipantsSerializer

from .filters import QuizFilter
from .models import Answer, Question, Quiz
from .serializers import QuizCreateSerializer, QuizDetailsSerializer, QuizListSerializer

User = get_user_model()


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
    permission_classes = (permissions.IsAuthenticated,)
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


class QuizOwnedInviteParticipantsViewset(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = QuizOwnedInviteParticipantsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # NOTE ONLY for internal users. Next steps could be creating register endpoint and sending inv with link to it

    def create(self, request, *args, **kwargs):
        serializer = QuizOwnedInviteParticipantsSerializer(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid(raise_exception=True):
            emails = serializer.validated_data.get("emails")
            existing_users = User.objects.filter(email__in=emails)
            existing_emails = list(existing_users.values_list("email", flat=True).distinct())
            # existing_emails = [email for email in emails if User.objects.filter(email=email).exists()]
            if existing_users:
                quiz = Quiz.objects.get(id=kwargs.get("owned_pk"))
                QuizInvitation.objects.bulk_create(
                    [
                        QuizInvitation(owner=quiz.owner, invited=user, quiz=quiz, status=StatusChoices.SENT.value)
                        for user in existing_users
                    ]
                )

                subject = "You have beed invitied to the quiz!"
                message = f"You have beed invited by '{quiz.owner.full_name}' to the quiz named '{quiz.name}'."

                # send_mail(
                #     subject=subject,
                #     message=message,
                #     from_email=settings.EMAIL_HOST_USER,
                #     recipient_list=existing_emails,
                #     # fail_silently=False,
                # )
                # NOTE return only filtered values
                return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)
            return Response("Email address(es) wasn't find in the database.", status=status.HTTP_400_BAD_REQUEST)
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
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = QuizFilter

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    def get_serializer_class(self):
        if self.action in ["list"]:
            return QuizListSerializer
        elif self.action in ["retrieve"]:
            return QuizDetailsSerializer

    # NOTE: add more tests, crucial ones
    # NOTE: optimalization of endpoints
