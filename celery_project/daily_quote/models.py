import logging

from django.db import models

from model_utils.models import TimeStampedModel

logger = logging.getLogger(__name__)


class Quote(TimeStampedModel):
    """
    A Quote to display on the home page
    """

    quote = models.TextField("Quote")
    author_name = models.CharField("Author", max_length=255)

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"
        ordering = ["-created"]

    def __str__(self):
        return self.quote
