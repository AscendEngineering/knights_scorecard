from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
import json
from .models import *
import datetime
from pytz import timezone
from .userManager import *


def test(request):
    return HttpResponse("test")

def splashPage(request):
    return render(request,'splash.html')

def mainPage(request):
    return render(request, 'index.html')

@csrf_exempt
def knightsPage(request):

    if request.method == 'GET':
        name = request.GET.get('name')
        context = {"name": name}
        return render(request, 'knights.html',context)

    else:
        return HttpResponse(status=400)

@csrf_exempt
def getMetrics(request):

    days = request.GET.get('days_ago','0')

    #get the token to access the data
    current_token = ""
    try:
        current_gid = request.session.__getitem__("gid")
        current_knight = knight(current_gid)
        
        if(current_knight.token_expired()):
            return []
        else:
            current_token=current_knight.get("token")

    except KeyError as err:
        print("Error finding user session credentials",err)
        return []

    #get past events
    sdate,edate = getPastDates(int(days))
    pastEvents = getCalendarData("VM Reminder",sdate,edate)

    #get future events
    sdate,edate = getFutureDates(int(days))
    futureEvents = getCalendarData("VM Reminder",sdate,edate)

    #run the data through metrics processor


    #form response json
    retVal = {
        "Days": days, 
        "Past Meetings": str(len(pastEvents)),
        "Future Meetings": str(len(futureEvents))
    }

    #return that json
    return(JsonResponse(retVal))

@csrf_exempt       
def authenticateUser(request):

    if request.method=='POST':
        

        #get all the info of the user (ID,Full Name, email, ID Token)
        user_data = request.POST.dict()

        #TODO authorize with google that this is a valid token
        
        #authenticate user
        current_knight = knight(user_data["gid"])
        if(current_knight.exists() and (not current_knight.token_expired())):
            print("User:", current_knight,"|",user_data["name"])
            request.session.__setitem__("gid",current_knight.get("gid"))
            return HttpResponse("authorized")
        else:
            #store the client's credentials
            succ = current_knight.make(user_data)

            if(succ):
                request.session.__setitem__("gid",current_knight.get("gid"))
                return HttpResponse("authorized")
            else:
                return HttpResponse(status=401)

    
    else:
        return HttpResponse("Should be a POST method for authorization",status=500)


@csrf_exempt
def authorizeUser(request):
    #serve up the webpage that will will tell the user to authenticate our services
    print("TODO")

    return HttpResponse("Need to authorize")

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