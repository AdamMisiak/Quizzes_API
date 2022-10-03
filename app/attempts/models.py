from django.db import models
from django_extensions.db.models import TimeStampedModel


class Attempt(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="attempts")
    quiz = models.ForeignKey("quizzes.Quiz", on_delete=models.CASCADE, related_name="attempts")

    class Meta:
        verbose_name = "Attempt"
        verbose_name_plural = "Attempts"

    def __str__(self):
        return f"{self.id} - ATTEMPT"


class AttemptAnswer(models.Model):
    attempt = models.ForeignKey("attempts.Attempt", on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey("quizzes.Question", on_delete=models.CASCADE, related_name="attempts")
    answer = models.ForeignKey("quizzes.Answer", on_delete=models.CASCADE, related_name="attempts")
    # NOTE: signal or set in endpoint to answer the questions?
    is_correct = models.BooleanField(default=False, verbose_name=("is_correct"))
    created = models.DateTimeField(editable=False, blank=True, auto_now_add=True)

    class Meta:
        verbose_name = "Attempt Answer"
        verbose_name_plural = "Attempt Answers"

    def __str__(self):
        return f"{self.id} - ATTEMPT ANSWER"
