from django.shortcuts import render
from django.http import Http404, HttpResponseServerError

from celery_project.daily_quote.models import Quote


def view_daily_quote(request):
    try:
        quote_of_the_day = Quote.objects.all()[0]
        context_dict = {"daily_quote": quote_of_the_day}
    except IndexError:
        raise HttpResponseServerError("Oops! Looks like the quote stash is empty!")
    except Quote.DoesNotExist:
        raise Http404("Oops! Looks like we don't have any quote for today")

    return render(request, "daily_quote/home.html", context_dict)
