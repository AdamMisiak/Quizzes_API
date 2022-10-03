import factory
from attempts.models import Attempt, AttemptAnswer
from faker import Faker

faker = Faker()


class AttemptFactory(factory.Factory):
    class Meta:
        model = Attempt


class AttemptAnswerFactory(factory.Factory):
    class Meta:
        model = AttemptAnswer
