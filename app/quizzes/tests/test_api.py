from django.urls import reverse
from quizzes.models import Question
from quizzes.tests.factories import AnswerFactory, QuestionFactory, QuizFactory
from rest_framework.test import APITestCase
from users.tests.factories import UserFactory


class QuizApiTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.save()
        # self.quiz = QuizFactory()
        # self.quiz.save()
        # self.question = QuestionFactory(content="1 + 1 = ?")
        # self.question.save()
        # self.question2 = QuestionFactory(content="How is current president of Poland?")
        # self.question2.save()

    def test_create_quiz(self):
        print(self.user)
        pass
