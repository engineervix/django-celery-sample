from config import celery_app

from celery_project.daily_quote.quotes import sync_quote_of_the_day


@celery_app.task(name="task_fetch_daily_quote")
def task_fetch_daily_quote():
    """Fetch Daily Quote, Save to Database & Delete Older Quote(s)"""
    print("Time to fetch Today's Quote")
    sync_quote_of_the_day()
