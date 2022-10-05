from attempts.tests.factories import AttemptAnswerFactory, AttemptFactory
from django.urls import reverse
from quizzes.models import Answer, Question, Quiz
from quizzes.tests.factories import AnswerFactory, QuestionFactory, QuizFactory
from rest_framework.test import APITestCase
from users.enums import StatusChoices
from users.tests.factories import QuizInvitationFactory, UserFactory


class QuizInvitationApiTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.save()
        self.user2 = UserFactory()
        self.user2.save()
        self.quiz = QuizFactory(owner=self.user2)
        self.quiz.save()
        self.quiz2 = QuizFactory(owner=self.user)
        self.quiz2.save()
        self.quiz_invitation = QuizInvitationFactory(owner=self.user2, invited=self.user, quiz=self.quiz)
        self.quiz_invitation.save()
        self.quiz_invitation2 = QuizInvitationFactory(owner=self.user, invited=self.user2, quiz=self.quiz2)
        self.quiz_invitation2.save()

    def test_get_all_quiz_invitations(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("api:invitations-list", args=["v1"])

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["id"], self.quiz_invitation.id)
        self.assertEqual(response.json()["results"][0]["owner"]["id"], self.user2.id)
        self.assertEqual(response.json()["results"][0]["quiz"]["id"], self.quiz.id)

    def test_accept_invitation(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("api:invitations-accept", args=["v1", self.quiz_invitation.id])

        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, 204)
        self.quiz_invitation.refresh_from_db()
        self.assertEqual(self.quiz_invitation.status, StatusChoices.ACCEPTED.value)
        self.assertTrue(self.user in self.quiz.participants.all())

    def test_reject_invitation(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("api:invitations-reject", args=["v1", self.quiz_invitation.id])

        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, 204)
        self.quiz_invitation.refresh_from_db()
        self.assertEqual(self.quiz_invitation.status, StatusChoices.REJECTED.value)
        self.assertFalse(self.user in self.quiz.participants.all())
