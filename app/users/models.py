from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .enums import StatusChoices
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=("first name"))
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=("last name"))
    is_staff = models.BooleanField(
        verbose_name=("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this site."),
    )
    is_active = models.BooleanField(
        verbose_name=("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    @property
    def full_name(self):
        first_name = self.first_name or ""
        last_name = self.last_name or ""
        return f"{first_name} {last_name}".strip()


class QuizInvitation(models.Model):
    # NOTE related names can be refactored
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="invites")
    invited = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="invited")
    quiz = models.ForeignKey("quizzes.Quiz", on_delete=models.CASCADE, related_name="invites")
    status = models.PositiveSmallIntegerField(
        verbose_name=("status"),
        choices=StatusChoices.choices,
        blank=True,
        null=True,
    )
    created = models.DateTimeField(editable=False, blank=True, auto_now_add=True)

    class Meta:
        verbose_name = "Quiz Invitation"
        verbose_name_plural = "Quiz Invitations"

    def __str__(self):
        return f"{self.id}: QUIZ INVITATION"
