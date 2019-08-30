from django.db import models
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import google.oauth2.credentials
import datetime
import os.path
import pickle


def expandTime(date,time):
    extratime = '-05:00'

    if(time.count(':')<2):
        extratime = ':00' + extratime

    return (date+'T'+ time + extratime)

def fillWriteTemplate(title,description,start_time,end_time):
    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Chicago',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Chicago',
        }
    }

    return event

def getCalendarData(email,token, search,sdate,edate):
    
    #sanity check
    if(token==""):
        return


    #form the start date
    sdatetime = sdate.split(' ')
    sdate = sdatetime[0]
    stime = sdatetime[1]
    start_time = expandTime(sdate,stime)

    #form the end date
    edatetime = edate.split(' ')
    edate = edatetime[0]
    etime = edatetime[1]
    end_time = expandTime(edate,etime)

    #create service
    creds = google.oauth2.credentials.Credentials(token)
    service = build('calendar', 'v3', credentials=creds)

    #execute the get from Google
    events_data = []
    page_token = None
    while True:

        try:
            events = service.events().list(calendarId=email, q=search, timeMin=start_time, timeMax=end_time, pageToken=page_token, singleEvents=True).execute()
            events_data.extend(events['items'])
            page_token = events.get('nextPageToken')
        except HttpError as err:
            print("Error requesting metrics from calendar")
            break

        if not page_token:
            break

    return events_data

#keeps track of the knights
class userInfo(models.Model):
    gid = models.CharField(max_length=63)
    access_token = models.CharField(max_length=4095)
    expires_at = models.CharField(max_length=63)
    name = models.CharField(max_length=63)
    email = models.CharField(max_length=511)

    def __str__(self):
        return self.gid

    def dict(self):
        return {
            "gid": self.gid,
            "access_token": self.access_token,
            "expires_at": self.expires_at,
            "name": self.name,
            "email": self.email
        }

#keeps track of the user's on the website
class knightInfo(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def dict(self):
        return{
            "name" : self.name,
            "email": self.email
        }
    
