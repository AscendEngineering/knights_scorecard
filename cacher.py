from background_task import background
from django.contrib.auth.models import User
from social_django.utils import load_strategy
from scorecard.userManager import *
from scorecard.models import all_emails,getCalendarData
from knightsTracker.settings import METRICS,PERIODICALS

from scorecard.tools import get_gcal_url,getBEDates

import sys
import time
import datetime

sleepTime = 3600

while(True):
    for email in all_emails():

        manager = knight(email).get('acc_manager')

        #grab token
        try:
            user = User.objects.get(email=manager)
            social_acc = user.social_auth.get(provider='google-oauth2')
            current_token = social_acc.get_access_token(load_strategy())
        except:
            sys.stderr.write("Error updating " + email + ": Account Manager '" + manager + "' does not exist\n")
            continue
        
        #make requests from google
        for metric in METRICS:
            sdate,current_date,edate = getBEDates('M')

            pastEvents = len(getCalendarData(email,current_token,metric,sdate,current_date))
            futureEvents = len(getCalendarData(email,current_token,metric,current_date,edate))

            knight(email).update_cache(metric,'M',pastEvents,futureEvents)
        print(email, "cache updated")
    
    print("Cache finished updating", str(datetime.datetime.now()) +"-5:00\n")
    time.sleep(sleepTime)

    
    



