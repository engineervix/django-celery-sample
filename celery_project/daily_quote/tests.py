from django.apps import apps

import pytest

from celery_project.daily_quote.tasks import task_fetch_daily_quote
from celery_project.daily_quote.models import Quote
from celery_project.daily_quote.apps import DailyQuoteConfig


@pytest.mark.celery
@pytest.mark.django_db
def test_daily_quote_fetch():
    initial_quotes = Quote.objects.all()
    # we created 2 quotes in conftest.py
    assert initial_quotes.count() == 2

    task_fetch_daily_quote()

    updated_quotes = Quote.objects.all()
    # if the task ran, there should be only 1 quote in the DB
    assert updated_quotes.count() == 1


@pytest.mark.django_db
def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "daily_quote/home.html" in [t.name for t in response.templates]
    assert b'<h2 class="font-weight-light">Today is' in response.content


@pytest.mark.django_db
def test_daily_quote_app():
    assert DailyQuoteConfig.name == "celery_project.daily_quote"
    assert apps.get_app_config("daily_quote").name == "celery_project.daily_quote"
