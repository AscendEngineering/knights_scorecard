import datetime
from .userManager import site_user
from pytz import timezone
from django.http import HttpResponse
import calendar
from django.shortcuts import redirect
from scorecard.userManager import knight
from knightsTracker.settings import PERIODICALS

def get_gcal_url(email):
    return "https://calendar.google.com/calendar/embed?src=" + email + "&ctz=America%2FChicago"


#move this method somewhere else
def authenticateUser(backend, details, response, uid, user, *args, **kwargs):

    #check if they are authorized (paying us money)
    if(site_user(uid).exists()):
        site_user(uid).loggedOn()
    else:
        return redirect("/access_denied")



def getBEDates(periodical,curr_timezone='America/Chicago'):
    periodical = periodical.upper()

    if(periodical not in PERIODICALS):
        return None

    #vars
    current_date = datetime.datetime.now().replace(tzinfo=timezone(curr_timezone))
    sdate = datetime.datetime(year=current_date.year,month=1,day=1,tzinfo=timezone(curr_timezone))
    edate = datetime.datetime(year=current_date.year,month=1,day=1,tzinfo=timezone(curr_timezone))

    #set dates
    if (periodical=='A'):
        edate = edate.replace(year=current_date.year+1)

    elif (periodical=='M'):
        sdate = sdate.replace(month=current_date.month)
        last_day_of_month = calendar.monthrange(current_date.year, current_date.month)[-1]
        edate = edate.replace(month=current_date.month, day = last_day_of_month)

    else:
        sdate = sdate.replace(month=current_date.month, day=current_date.day)
        edate = edate.replace(month=current_date.month, day=current_date.day+1)

    
    sdate_output = sdate.strftime("%Y-%m-%dT%H:%M:%S" )+ '-00:00'
    edate_output = edate.strftime("%Y-%m-%dT%H:%M:%S" )+ '-00:00'
    current_output = current_date.strftime("%Y-%m-%dT%H:%M:%S" )+ '-00:00'

    return sdate_output,current_output,edate_output

def getCachedData(email,metric,periodical):
    key = metric + "|" + periodical
    try:
        cached_data = knight(email).get_cached()
        event_values = cached_data[key]
    except KeyError as err:
        print("No cached data exists for key:", key)
        return 0,0
    return event_values[0],event_values[1]
