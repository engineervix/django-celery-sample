#!/usr/bin/env python3

"""quotery.py

This script is part of a daily celery task to fetch a quote
from a JSON file and save it to the database.

There should only be one quote at a time in the database.

On the template, we simply retrieve the quote and
display it on the website as "Quote of the Day".

The idea is to have a drop-in script that simulates an API call
so that in future, if we find a suitable quote API, we can easily
refactor accordingly and use the new API, without making significant
changes to the codebase.
"""

import os
import logging
import traceback
import re
from datetime import datetime
import json

from celery_project.daily_quote.models import Quote

logger = logging.getLogger(__name__)


def quote_index(start_date):
    """
    Determine which quote (index) to retrieve from the given JSON file
    based on the current date.

    Args:
        start_date (str): the reference start date in YYYY-MM-DD format.
            This date corresponds to index 0.

    Returns:
        int: the index to retrieve

    """
    today = datetime.today()
    date_format = "%Y-%m-%d"
    try:
        initial_date = datetime.strptime(start_date, date_format)
    except ValueError:
        var = traceback.format_exc()
        logger.error(var)
        initial_date = datetime(2021, 3, 1)
    days_since_start = (today - initial_date).days
    idx = days_since_start

    return abs(idx)  # in case we have a negative int!


def quote_of_the_day():
    """
    let's get that quote
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_file = os.path.join(dir_path, "quotes.json")

    with open(json_file, "r") as read_file:
        data = json.load(read_file)

    num_of_quotes = len(data)
    idx = quote_index("2021-03-01")
    while idx >= num_of_quotes:
        idx = idx - num_of_quotes

    quote = data[idx]

    return quote


def sync_quote_of_the_day():
    """
    We get our quote and save it to our Quote Model in the Database
    We then delete older entry(ies)
    """
    qod = quote_of_the_day()
    # lets make sure we don't save the same entry more than once
    if not Quote.objects.filter(quote=qod["text"]).exists():
        quote_entry = Quote(
            quote=qod["text"],
            author_name=qod["author"],
        )
        quote_entry.save()
        # Quote.objects.filter(created__lt=datetime.today()).delete()
        # delete all but first:
        Quote.objects.filter(
            id__in=list(Quote.objects.values_list("pk", flat=True)[1:])
        ).delete()
