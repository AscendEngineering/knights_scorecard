from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
import json
from .models import *


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
        name = request.POST.get('name')
        print(json.loads(request.body.decode('utf-8')))
        postToCal(json.loads(request.body.decode('utf-8')),name)
        return(HttpResponse("created"))

    else:
        return HttpResponse(status=400)
        


