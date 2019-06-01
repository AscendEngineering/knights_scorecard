from django.db import models
from oauth2client import client
from googleapiclient import sample_tools
import datetime


def formatTime(oldtime):
    newtime = oldtime
    newtime = newtime.replace(" ","T")
    newtime = newtime[:newtime.find('.')] + '-07:00'
    return newtime


def expandTime(date,time):
    return (date+'T'+time+':00-06:00')

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

# Create your models here.
def postToCal(formData):

    #variables
    start_time = expandTime(formData["date"],formData["time"])
    end_time = expandTime(formData["date"],"17:30") #this is going to have to change/be more dynamic
    title = "Bob's Meeting with " + formData['client_name']
    description = formData['client_details']

    #create the service
    service, flags = sample_tools.init([], 'calendar', 'v3', __doc__, __file__, scope='https://www.googleapis.com/auth/calendar')

    event = fillTemplate(title,description,start_time,end_time)
    #event = service.events().get(calendarId='stainless809@gmail.com', eventId='0ef72rn5h51uhdbghg7vivepgj').execute()
    event = service.events().insert(calendarId='stainless809@gmail.com', body=event).execute()

    print(event)
    #print('Event created: %s' % (event.get('htmlLink')))

    return "Todo"



    