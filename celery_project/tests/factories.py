from celery_project.users.models import User
import factory


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
