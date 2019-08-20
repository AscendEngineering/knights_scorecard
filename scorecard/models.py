from django.db import models
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
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

#this is outdated and needs to be deleted
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

def getCalendarData(search,token,sdate,edate):
    
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

    #get the current gid
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

    #create service
    creds = google.oauth2.credentials.Credentials(current_token)
    service = build('calendar', 'v3', credentials=creds)
    print("Created service with token",current_token)

    #execute the get from Google
    events_data = []
    page_token = None
    while True:
        events = service.events().list(calendarId='stainless809@gmail.com', q=search, timeMin=start_time, timeMax=end_time, pageToken=page_token).execute()
        events_data.extend(events['items'])
        page_token = events.get('nextPageToken')
        if not page_token:
            break

    return events_data

#keeps track of the knights
class knightInfo(models.Model):
    gid = models.CharField(max_length=63)
    access_token = models.CharField(max_length=4095)
    expires_at = models.CharField(max_length=63)
    name = models.CharField(max_length=63)
    email = models.CharField(max_length=511)

    def __str__(self):
        return self.kid

#keeps track of the user's on the website
class userInfo(models.Model):
    gid = models.CharField(max_length=63)
    idToken = models.CharField(max_length=4096)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    

    def __str__(self):
        return self.uid
