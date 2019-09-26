from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from social_django.utils import load_strategy
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import *
from .userManager import *
from .sessionManager import *
from .tools import get_gcal_url,getBEDates, getCachedData
import scorecard.klogging as LOG

import time
import json


def test(request):
    return HttpResponse("test")

def splashPage(request):
    google_login = request.user
    if(google_login.get_username() != ""):
        return (redirect("/main"))

    return render(request,'splash.html')

def access_denied(request):
    return HttpResponse(status=403)

@login_required
def mainPage(request):
    return render(request, 'index.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect("/")

@login_required
def knightsPage(request):

    if request.method == 'GET':
        name = request.GET.get('name')

        #get the email
        email = knight(name).get("email")

        context = {"name": name, "email": get_gcal_url(email)}
        return render(request, 'knights.html',context)

    else:
        return HttpResponse(status=400)


@login_required
def getKnights(request):
    retVal=[]

    #return the list of knights
    try:
        allknights = knightInfo.objects.all()
        for knight in allknights:
            retVal.append(knight.name)
    except AttributeError as err:
        LOG.error("Error Accessing Knights emails: " + str(err))

    return(JsonResponse({"knights":retVal}))

@login_required
def getMetrics(request):

    periodical = request.GET.get('periodical','M')
    name = request.GET.get('name','')
    metric = request.GET.get('metric','')
    cached = request.GET.get('cached','')

    LOG.info("Fetching " + metric + " for " + name + " with " + periodical + " frequency")
  
    #grab the current token
    google_login = request.user.social_auth.get(provider="google-oauth2")
    current_token = google_login.get_access_token(load_strategy())

    #select the matching knight
    knight_emails = []
    if(name=="all"):
        knight_emails = all_emails()
    else:
        knight_emails.append(knight(name).get("email"))

    #variables
    totalFutureEvents = 0
    totalPastEvents = 0

    for email in knight_emails:

        #get dates
        sdate,current_date,edate = getBEDates(periodical)

        #get events
        if(cached==''):
            pastEvents = len(getCalendarData(email,current_token,metric, sdate,current_date))
            futureEvents = len(getCalendarData(email,current_token,metric, current_date,edate))
        else:
            pastEvents,futureEvents = getCachedData(email,metric,periodical)

        #cache the results
        knight(email).update_cache(metric,periodical,pastEvents,futureEvents)

        #add them to total
        totalPastEvents+=pastEvents
        totalFutureEvents+=futureEvents

    #form response json
    retVal = {
        "Meeting": metric, 
        "Previous Appointments (1st)": str(totalPastEvents),
        "Future Appointments (EOM)": str(totalFutureEvents)
    }

    #return that json
    return(JsonResponse(retVal))
     


    
    
