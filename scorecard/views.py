from django.shortcuts import render
from django.http import HttpResponse

def test(request):
    return HttpResponse("test")

def mainPage(request):
    return render(request, 'index.html')
