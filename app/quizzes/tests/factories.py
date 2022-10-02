import factory
from faker import Faker
from quizzes.models import Answer, Question, Quiz

faker = Faker()


class QuizFactory(factory.Factory):
    class Meta:
        model = Quiz

    name = factory.LazyFunction(lambda: faker.text(max_nb_chars=100))


class QuestionFactory(factory.Factory):
    class Meta:
        model = Question

    content = factory.LazyFunction(lambda: faker.text(max_nb_chars=100))


class AnswerFactory(factory.Factory):
    class Meta:
        model = Answer

    content = factory.LazyFunction(lambda: faker.text(max_nb_chars=10))
    is_correct = Faker().pybool()
