from django.db import models
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import google.oauth2.credentials
import datetime
import os.path
import pickle
import scorecard.klogging as LOG
from scorecard.userManager import knight

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

def getCachedData(email,metric,periodical):
    cached_data = knight(email).get_cached()
    key = metric + "|" + periodical
    event_values = cached_data[key]
    return event_values[0],event_values[1]


def getCalendarData(email,token, search,sdate,edate):
    
    #sanity check
    if(token==""):
        return

    #create service
    creds = google.oauth2.credentials.Credentials(token)
    service = build('calendar', 'v3', credentials=creds)

    #execute the get from Google
    events_data = []
    page_token = None
    while True:

        try:
            events = service.events().list(calendarId=email, q=search, timeMin=sdate, timeMax=edate, pageToken=page_token, singleEvents=True).execute()
            events_data.extend(events['items'])
            page_token = events.get('nextPageToken')
        except HttpError as err:
            LOG.error("Not authorized: " + email + "|" + search)
            break

        if not page_token:
            break

    return events_data


def all_emails():
    retVal = []
    allKnightsInfo = knightInfo.objects.all()
    for knight in allKnightsInfo:
        retVal.append(knight.dict()["email"])
    return retVal


#keeps track of the knights
class userInfo(models.Model):
    name = models.CharField(max_length=63)
    email = models.CharField(max_length=511)
    timesLoggedIn = models.IntegerField()

    def __str__(self):
        return self.dict()

    def dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "timesLoggedIn": self.timesLoggedIn
        }

#keeps track of the user's on the website
class knightInfo(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    metric_cache = models.TextField()

    def __str__(self):
        return self.name

    def dict(self):
        return{
            "name" : self.name,
            "email": self.email,
            "metric_cache": self.metric_cache
        }
    
