import factory
from faker import Faker
from users.enums import StatusChoices
from users.models import QuizInvitation, User

faker = Faker()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user_{n}@email.com")
    first_name = factory.LazyFunction(lambda: faker.first_name())
    last_name = factory.LazyFunction(lambda: faker.last_name())
    is_superuser = False


class QuizInvitationFactory(factory.Factory):
    class Meta:
        model = QuizInvitation

    status = StatusChoices.SENT.value
