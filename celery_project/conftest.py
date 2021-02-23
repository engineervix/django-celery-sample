import pytest
import factory
from django.conf import settings
from faker import Faker

from celery_project.tests.factories import UserFactory

fake = Faker()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker, tmpdir_factory):
    """
    Configure the DB for Testing.
    We also configure a MEDIA_ROOT temporary directory
    """
    media_dir = "_media_store"
    media_storage = tmpdir_factory.mktemp(media_dir)
    tmpdir_factory.mktemp(media_dir).join("images")
    tmpdir_factory.mktemp(media_dir).join("original_images")
    settings.MEDIA_ROOT = str(media_storage)
    with django_db_blocker.unblock():
        # create superuser
        UserFactory(
            is_staff=True,
            is_superuser=True,
        )
