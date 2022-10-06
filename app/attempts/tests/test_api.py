from django.urls import reverse
from quizzes.tests.factories import AnswerFactory, QuestionFactory, QuizFactory
from rest_framework.test import APITestCase
from users.tests.factories import UserFactory


class QuizInvitationApiTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.save()
        self.user2 = UserFactory()
        self.user2.save()
        self.quiz = QuizFactory(owner=self.user)
        self.quiz.save()
        self.quiz.participants.add(self.user2)
        self.question = QuestionFactory(quiz=self.quiz)
        self.question.save()
        self.answer = AnswerFactory(question=self.question, is_correct=False)
        self.answer.save()
        self.answer2 = AnswerFactory(question=self.question, is_correct=True)
        self.answer2.save()
        self.question2 = QuestionFactory(quiz=self.quiz)
        self.question2.save()
        self.answer3 = AnswerFactory(question=self.question2, is_correct=False)
        self.answer3.save()
        self.answer4 = AnswerFactory(question=self.question2, is_correct=True)
        self.answer4.save()

    def test_attempt_invited_quiz_succeed(self):
        self.assertEqual(self.user2.attempts.count(), 0)
        self.client.force_authenticate(user=self.user2)
        url = reverse("api:quizzes-invited-attempt-list", args=["v1", self.quiz.id])
        data = {
            "answers": [
                {"question": self.question.id, "answer": self.answer2.id},
                {"question": self.question2.id, "answer": self.answer4.id},
            ]
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.user2.attempts.count(), 1)
        self.assertEqual(self.user2.attempts.first().quiz, self.quiz)
        self.assertTrue(self.user2.attempts.first().is_finished)
        self.assertTrue(self.user2.attempts.first().is_successful)
        self.assertEqual(self.user2.attempts.first().answers.count(), 2)

    def test_attempt_invited_quiz_finished(self):
        self.assertEqual(self.user2.attempts.count(), 0)
        self.client.force_authenticate(user=self.user2)
        url = reverse("api:quizzes-invited-attempt-list", args=["v1", self.quiz.id])
        data = {
            "answers": [
                {"question": self.question.id, "answer": self.answer2.id},
                {"question": self.question2.id, "answer": self.answer3.id},
            ]
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.user2.attempts.count(), 1)
        self.assertEqual(self.user2.attempts.first().quiz, self.quiz)
        self.assertTrue(self.user2.attempts.first().is_finished)
        self.assertFalse(self.user2.attempts.first().is_successful)
        self.assertEqual(self.user2.attempts.first().answers.count(), 2)

    def test_attempt_invited_quiz_not_finished(self):
        self.assertEqual(self.user2.attempts.count(), 0)
        self.client.force_authenticate(user=self.user2)
        url = reverse("api:quizzes-invited-attempt-list", args=["v1", self.quiz.id])
        data = {
            "answers": [
                {"question": self.question.id, "answer": self.answer2.id},
            ]
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.user2.attempts.count(), 1)
        self.assertEqual(self.user2.attempts.first().quiz, self.quiz)
        self.assertFalse(self.user2.attempts.first().is_finished)
        self.assertFalse(self.user2.attempts.first().is_successful)
        self.assertEqual(self.user2.attempts.first().answers.count(), 1)
