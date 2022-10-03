from django.urls import reverse
from quizzes.tests.factories import AnswerFactory, QuestionFactory, QuizFactory
from rest_framework.test import APITestCase
from users.tests.factories import UserFactory


class QuizFilterTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.save()
        self.quiz = QuizFactory(name="Math Quiz", owner=self.user)
        self.quiz.save()
        self.question = QuestionFactory(content="1+1=?", quiz=self.quiz)
        self.question.save()
        self.answer = AnswerFactory(content="1", is_correct=False, question=self.question)
        self.answer.save()
        self.answer2 = AnswerFactory(content="2", is_correct=True, question=self.question)
        self.answer2.save()
        self.question2 = QuestionFactory(content="10-5=?", quiz=self.quiz)
        self.question2.save()
        self.answer3 = AnswerFactory(content="3", is_correct=False, question=self.question2)
        self.answer3.save()
        self.answer4 = AnswerFactory(content="5", is_correct=True, question=self.question2)
        self.answer4.save()

        self.quiz2 = QuizFactory(name="Geological Quiz", owner=self.user)
        self.quiz2.save()
        self.question3 = QuestionFactory(content="What is the capital city of the Poland?", quiz=self.quiz2)
        self.question3.save()
        self.answer5 = AnswerFactory(content="Warsaw", is_correct=False, question=self.question3)
        self.answer5.save()
        self.answer6 = AnswerFactory(content="Cracow", is_correct=True, question=self.question3)
        self.answer6.save()
        self.question4 = QuestionFactory(content="Which city is the biggest?", quiz=self.quiz2)
        self.question4.save()
        self.answer7 = AnswerFactory(content="London", is_correct=False, question=self.question4)
        self.answer7.save()
        self.answer8 = AnswerFactory(content="Manchester", is_correct=True, question=self.question4)
        self.answer8.save()
        self.answer9 = AnswerFactory(content="Edynburg", is_correct=True, question=self.question4)
        self.answer9.save()

    def test_filter_owned_quizzes(self):
        url = reverse("api:quizzes-owned-list", args=["v1"])
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url, {"search": "edyn"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["results"][0]["id"], self.quiz2.id)

        response = self.client.get(url, {"search": "capital"})
        self.assertEqual(response.json()["results"][0]["id"], self.quiz2.id)

        response = self.client.get(url, {"search": "randomvalue"})
        self.assertEqual(response.json()["results"], [])

        response = self.client.get(url, {"name": "Math"})
        self.assertEqual(response.json()["results"][0]["id"], self.quiz.id)

        response = self.client.get(url, {"question": "10-5"})
        self.assertEqual(response.json()["results"][0]["id"], self.quiz.id)

        response = self.client.get(url, {"question": "biggest"})
        self.assertEqual(response.json()["results"][0]["id"], self.quiz2.id)

        response = self.client.get(url, {"answer": "don"})
        self.assertEqual(response.json()["results"][0]["id"], self.quiz2.id)

        response = self.client.get(url, {"answer": "5"})
        self.assertEqual(response.json()["results"][0]["id"], self.quiz.id)
