from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class User(AbstractUser):
    """Default user for the Daily Power Devotional"""

    username = None
    email = models.EmailField(_("email address"), unique=True)

    name = models.CharField(blank=True, max_length=255)

    USERNAME_FIELD = "email"
    # the email field and password will be required,
    # so they don’t need to go into the REQUIRED FIELDS list
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
