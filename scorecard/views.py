from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
import json
from .models import *
import datetime
from pytz import timezone


def test(request):
    return HttpResponse("test")

def mainPage(request):
    return render(request, 'index.html')

@csrf_exempt
def knightsPage(request):

    if request.method == 'GET':
        name = request.GET.get('name')
        context = {"name": name}
        return render(request, 'knights.html',context)
        
    elif request.method == 'POST':
        data_req = json.loads(request.body.decode('utf-8'))
        postToCal(data_req)
        return(HttpResponse("created"))

    else:
        return HttpResponse(status=400)

@csrf_exempt
def getMetrics(request):

    days = request.GET.get('days_ago','0')

    #get past events
    sdate,edate = getPastDates(int(days))
    pastEvents = getCalendarData(request.GET.get('name',''),sdate,edate)

    #get future events
    sdate,edate = getFutureDates(int(days))
    futureEvents = getCalendarData(request.GET.get('name',''),sdate,edate)

    #run the data through metrics processor


    #form response json
    retVal = {
        "Days": days, 
        "Past Meetings": str(len(pastEvents)),
        "Future Meetings": str(len(futureEvents))
    }

    #return that json
    return(JsonResponse(retVal))
        

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