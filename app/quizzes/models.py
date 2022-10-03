from django.db import models
from django_extensions.db.models import TimeStampedModel

# from django.utils.translation import ugettext_lazy as _


class Quiz(TimeStampedModel):
    name = models.CharField(max_length=500)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="quizzes")
    participants = models.ManyToManyField("users.User", blank=True)

    # @property
    # def numer_of_attempts(self):
    #     return self.attempts.count()

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return f"{self.id} - {self.name} - QUIZ"


class Question(TimeStampedModel):
    quiz = models.ForeignKey("quizzes.Quiz", on_delete=models.CASCADE, related_name="questions")
    content = models.CharField(max_length=5000)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return f"{self.id} - {self.content} - QUESTION"


class Answer(TimeStampedModel):
    question = models.ForeignKey("quizzes.Question", on_delete=models.CASCADE, related_name="answers")
    content = models.CharField(max_length=5000)
    is_correct = models.BooleanField(default=False, verbose_name=("is_correct"))

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return f"{self.id} - {self.content} - ANSWER"
