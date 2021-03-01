from celery_project.users.models import User
import factory

from celery_project.daily_quote.models import Quote


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating Django User objects"""

    # username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    # is_staff = True
    # is_superuser = True

    class Meta:
        model = User


class QuoteFactory(factory.django.DjangoModelFactory):
    """Factory for creating Quote objects"""

    quote = factory.Faker("text")
    author_name = factory.Faker("name")

    class Meta:
        model = Quote
