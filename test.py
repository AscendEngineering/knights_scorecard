from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import google.oauth2.credentials
from django.contrib.auth.models import User
from social_django.utils import load_strategy



#create service
user = User.objects.get(email="stainless809@gmail.com")
social_acc = user.social_auth.get(provider='google-oauth2')
current_token = social_acc.get_access_token(load_strategy())
print(current_token)
creds = google.oauth2.credentials.Credentials(current_token)
service = build('calendar', 'v3', credentials=creds)

page_token = None
while True:
  calendar_list = service.calendarList().list(pageToken=page_token).execute()
  for calendar_list_entry in calendar_list['items']:
    print(calendar_list_entry['summary'])
  page_token = calendar_list.get('nextPageToken')
  if not page_token:
    break