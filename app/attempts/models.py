from django.db import models
from django_extensions.db.models import TimeStampedModel


class Attempt(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="attempts")
    quiz = models.ForeignKey("quizzes.Quiz", on_delete=models.CASCADE, related_name="attempts")

    class Meta:
        verbose_name = "Attempt"
        verbose_name_plural = "Attempts"

    def __str__(self):
        return f"{self.id} - {self.user} - {self.quiz} - ATTEMPT"
