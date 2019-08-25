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

        #get the email
        email = knight(name).get("email")

        context = {"name": name, "email": get_gcal_url(email)}
        return render(request, 'knights.html',context)

    else:
        return HttpResponse(status=400)


@csrf_exempt
def getKnights(request):
    retVal=[]

    #return the list of knights
    try:
        allknights = knightInfo.objects.all()
        for knight in allknights:
            retVal.append(knight.name)
    except:
        print("Error Accessing Knights emails")

    return(JsonResponse({"knights":retVal}))

@csrf_exempt
def getMetrics(request):

    days = request.GET.get('days_ago','0')
    name = request.GET.get('name','')
    current_gid = session(request).get("gid")

    print("Name for metrics",name)

    #make sure gid exists
    if(current_gid == None):
        print("no gid")
        return HttpResponse(status=401)

    #select the matching user
    current_user = user(current_gid)
    current_token = ""
        
    if(current_user.token_expired()):
        print("token expired")
        return HttpResponse(status=401)
    else:
        current_token=current_user.get("access_token")


    #select the matching knight
    knight_email = knight(name).get("email")

    #get past events
    sdate,edate = getPastDates(int(days))
    pastEvents = getCalendarData(knight_email,current_token,"Krav", sdate,edate)

    #get future events
    sdate,edate = getFutureDates(int(days))
    futureEvents = getCalendarData(knight_email,current_token,"Krav", sdate,edate)

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
        current_user = user(user_data["gid"])
        if(current_user.exists() and (not current_user.token_expired())):
            session(request).set("gid",current_user.get("gid"))
            return HttpResponse("authorized")
        else:
            
            #store the client's credentials
            succ = current_user.make(user_data)

            if(succ):
                session(request).set("gid",current_user.get("gid"))
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

