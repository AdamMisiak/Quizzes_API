from django.urls import reverse
from quizzes.models import Answer, Question, Quiz
from rest_framework.test import APITestCase
from users.tests.factories import UserFactory


class QuizApiTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.save()

    def test_create_quiz(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("api:quizzes-list", args=["v1"])
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
