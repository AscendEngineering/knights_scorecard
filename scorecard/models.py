from django.db import models
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import os.path
import pickle


def formatTime(oldtime):
    newtime = oldtime
    newtime = newtime.replace(" ","T")
    newtime = newtime[:newtime.find('.')] + '-07:00'
    return newtime


def expandTime(date,time):
    return (date+'T'+time+':00-05:00')

def fillTemplate(title,description,start_time,end_time):
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


def getCredentials():

    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

# Create your models here.
def postToCal(formData, knight):

    #variables
    start_time = expandTime(formData["date"],formData["time"])
    end_time = expandTime(formData["date"],"17:30") #this is going to have to change/be more dynamic
    title = knight + " Meeting with " + formData['client_name']
    description = formData['client_details']

    #create the service
    creds = getCredentials()
    service = build('calendar', 'v3', credentials=creds)

    #execute the calendar event
    event = fillTemplate(title,description,start_time,end_time)
    event = service.events().insert(calendarId='stainless809@gmail.com', body=event).execute()

    if(event.status=='confirmed'):
        return True
    else:
        return False



    