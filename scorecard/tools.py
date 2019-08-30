import datetime
from pytz import timezone


def get_gcal_url(email):
    return "https://calendar.google.com/calendar/embed?src=" + email + "&ctz=America%2FChicago"


def getPastDates(days_ago):

    #get start and end dates
    today = datetime.datetime.now().replace(tzinfo=timezone('US/Central'))
    edate = datetime.datetime(today.year, today.month, today.day)
    sdate = datetime.datetime(today.year, today.month, today.day) - datetime.timedelta(days_ago)

    return str(sdate),str(edate)

def getFutureDates(days_future):

    #get start and end dates
    today = datetime.datetime.now().replace(tzinfo=timezone('US/Central'))
    sdate = datetime.datetime(today.year, today.month, today.day)
    edate = datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(days_future)

    return str(sdate),str(edate)