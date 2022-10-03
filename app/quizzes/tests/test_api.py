from attempts.tests.factories import AttemptAnswerFactory, AttemptFactory
from django.urls import reverse
from quizzes.models import Answer, Question, Quiz
from quizzes.tests.factories import AnswerFactory, QuestionFactory, QuizFactory
from rest_framework.test import APITestCase
from users.tests.factories import UserFactory


class QuizOwnedApiTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.save()

    def test_create_owned_quiz(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("api:quizzes-owned-list", args=["v1"])
        data = {
            "name": "Math quiz number 2",
            "questions": [
                {
                    "content": "1 + 1 = ?",
                    "answers": [{"content": "1", "is_correct": "False"}, {"content": "2", "is_correct": "True"}],
                }
            ],
        }
        response = self.client.post(url, data, format="json")
        # NOTE parameterized can be implemented here

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)
        self.assertEqual(Quiz.objects.count(), 1)
        self.assertEqual(Quiz.objects.first().name, data["name"])
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.first().content, data["questions"][0]["content"])
        self.assertEqual(Answer.objects.count(), 2)
        self.assertEqual(Answer.objects.first().content, data["questions"][0]["answers"][0]["content"])
        self.assertEqual(Answer.objects.last().content, data["questions"][0]["answers"][1]["content"])

    def test_get_owned_quizzes_list(self):
        self.quiz = QuizFactory(owner=self.user)
        self.quiz.save()
        self.question = QuestionFactory(quiz=self.quiz)
        self.question.save()
        self.answer = AnswerFactory(question=self.question, is_correct=True)
        self.answer.save()

        self.client.force_authenticate(user=self.user)
        url = reverse("api:quizzes-owned-list", args=["v1"])
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["results"][0]["name"], self.quiz.name)
        self.assertEqual(response.json()["results"][0]["owner"]["id"], self.quiz.owner.id)
        self.assertEqual(response.json()["results"][0]["questions"][0]["id"], self.question.id)
        self.assertEqual(response.json()["results"][0]["questions"][0]["answers"][0]["id"], self.answer.id)

    def test_get_owned_quiz_details(self):
        self.user2 = UserFactory()
        self.user2.save()
        self.quiz = QuizFactory(owner=self.user)
        self.quiz.save()
        self.quiz.participants.add(self.user2)
        self.question = QuestionFactory(quiz=self.quiz)
        self.question.save()
        self.answer = AnswerFactory(question=self.question)
        self.answer.save()

        self.attempt = AttemptFactory(user=self.user2, quiz=self.quiz)
        self.attempt.save()
        self.attempt_answer = AttemptAnswerFactory(
            attempt=self.attempt, question=self.question, answer=self.answer, is_correct=True
        )
        self.attempt_answer.save()

        self.client.force_authenticate(user=self.user)
        url = reverse("api:quizzes-owned-detail", args=["v1", self.quiz.id])
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], self.quiz.name)
        self.assertEqual(response.json()["owner"]["id"], self.quiz.owner.id)
        self.assertEqual(response.json()["questions"][0]["id"], self.question.id)
        self.assertEqual(response.json()["questions"][0]["answers"][0]["id"], self.answer.id)
        self.assertEqual(response.json()["attempts"][0]["id"], self.attempt.id)
        self.assertEqual(response.json()["attempts"][0]["user"]["id"], self.user2.id)
        self.assertEqual(response.json()["attempts"][0]["answers"][0]["id"], self.attempt_answer.id)
