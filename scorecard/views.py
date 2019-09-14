from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
import json
from .models import *
from .userManager import *
from .sessionManager import *
from .tools import get_gcal_url,getPastDates,getFutureDates
from social_django.utils import load_strategy
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import time


def test(request):
    return HttpResponse("test")

def splashPage(request):
    return render(request,'splash.html')

@login_required
def mainPage(request):
    return render(request, 'index.html')

@login_required
def logout(request):
    request.user.delete()
    return render(request, 'logout.html')

@login_required
def knightsPage(request):

    if request.method == 'GET':
        name = request.GET.get('name')

        #get the email
        email = knight(name).get("email")
        print(get_gcal_url(email))

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
        print("Error Accessing Knights emails")
        print(err)

    return(JsonResponse({"knights":retVal}))

@login_required
def getMetrics(request):

    days = request.GET.get('days_ago','0')
    name = request.GET.get('name','')
    metric = request.GET.get('metric','')
  
    #grab the current token
    google_login = request.user.social_auth.get(provider="google-oauth2")
    current_token = google_login.extra_data["access_token"]
    print(current_token)

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

        #get past events
        sdate,edate = getPastDates(int(days))
        pastEvents = getCalendarData(email,current_token,metric, sdate,edate)

        #get future events
        sdate,edate = getFutureDates(int(days))
        futureEvents = getCalendarData(email,current_token,metric, sdate,edate)

        #run the data through metrics processor
        totalPastEvents+=len(pastEvents)
        totalFutureEvents+=len(futureEvents)

    #form response json
    retVal = {
        "Meeting": metric, 
        "Past Meetings": str(totalPastEvents),
        "Future Meetings": str(totalPastEvents)
    }

    #return that json
    return(JsonResponse(retVal))
     
def authenticateUser(request):

    #grab the current user
    current_user = request.user.social_auth.get(provider='google-oauth2')
    current_uid = current_user.uid

    #check that we have a valid password
    if(not request.user.has_usable_password()):
        request.user.set_password("placeholder")
        request.user.save()

    print("cehcking to see fi exists")

    #check if they are authorized (paying us money)
    if(user(current_uid).exists()):
        user(current_uid).loggedOn()
        return(HttpResponse(status=200))
    else:
        #if not logout and reject
        #logout(request)
        return(redirect("/logout"))

    
    




