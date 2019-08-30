from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']



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

def expandTime(date,time):
    return (date+'T'+time+':00-06:00')

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])

    title = "this is a test"
    description = "test descriptopm"
    start_time = expandTime('2019-05-05','17:00')
    end_time = expandTime('2019-05-05','17:30')

    event = fillTemplate(title,description,start_time,end_time)
    event = service.events().insert(calendarId='stainless809@gmail.com', body=event).execute()

    print('Event created: %s' % (event.get('htmlLink')))

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

if __name__ == '__main__':
    main()




# import sys
# import os
# import datetime
# from scorecard.models import *


# def main(argv):

#     newtime = formatTime(str(datetime.datetime.now()))

#     formdata = {'client_name': 'hey', 'client_details': 'sadfsadf', 'date': '2019-05-05', 'time': '17:00'}

    


# if __name__ == '__main__':
#     main(sys.argv)