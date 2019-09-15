import datetime
from .userManager import site_user
from pytz import timezone
from django.http import HttpResponse


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

#move this method somewhere else
def authenticateUser(backend, details, response, uid, user, *args, **kwargs):

    #check that we have a valid password
    if(not user.has_usable_password()):
        user.set_password("placeholder")
        user.save()

    #check if they are authorized (paying us money)
    if(site_user(uid).exists()):
        site_user(uid).loggedOn()
    else:
        return HttpResponse(status=403)



