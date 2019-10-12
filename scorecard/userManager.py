from scorecard.models import *
from django.core.exceptions import *
import time
import json
import scorecard.klogging as LOG

class site_user():

    def __init__(self,email):
        self.email = email

    #exists - returns whether the user exists or not
    def exists(self):
        
        try:
            user = userInfo.objects.get(email=self.email)
        except userInfo.DoesNotExist as err:
            LOG.error("UserManager exists error: " + str(err))
            return False
        
        if(user != None):
            return True
        else:
            return False

    #get_all - get all fields
    def get_all(self):
        try:
            user=userInfo.objects.get(email=self.email).dict()
            return user
        except:
            return None

    #get - get a specific field (returns None if it does not exist)
    def get(self,metric):
        user_info = self.get_all()

        retVal = ""
        if(user_info != None):
            try:
                retVal = user_info[metric]
            except KeyError as err:
                LOG.error("User metric does not exist: " + str(err))
                return None
        else:
            return None

        return retVal
        
    #user has logged on, increment log on number
    def loggedOn(self):
        
        try:
            user=userInfo.objects.get(email=self.email)
        except userInfo.DoesNotExist as err:
            LOG.error("User info does not exist: " + str(err))
            return

        #increment log on
        new_timesLoggedIn = int(user.timesLoggedIn) +1
        userInfo.objects.filter(email=self.email).update(timesLoggedIn=new_timesLoggedIn)
        
        


class knight():
    
    def __init__(self,name):
        self.name = name

    def getDBObject(self):
        if("@gmail" in self.name):
            #search on email
            return knightInfo.objects.get(email=self.name)
        else:
            firstname = self.name.split(' ')[0]
            lastname = self.name.split(' ')[1]
            return knightInfo.objects.all().filter(name__icontains=firstname).get(name__icontains=lastname)

    #get_all - get all fields
    def get_all(self):
        try:
            return self.getDBObject().dict()
        except knightInfo.DoesNotExist as err:  
            LOG.error("Knight does not exist: " + str(err))
            return None

    #get - get a specific field (returns None if it does not exist)
    def get(self,metric):
        knight_info = self.get_all()

        retVal = ""
        if(knight_info != None):
            try:
                retVal = knight_info[metric]
            except KeyError as err:
                LOG.error("Knights metric does not exist: " + str(err))
                return None
        else:
            return None

        return retVal
        

    def update_cache(self, metric, period, pastEvents, futureEvents):
        knight=self.getDBObject()
        cached_info = self.get('metric_cache')

        if knight != None and cached_info != None:
            key = metric+"|"+period
            value = [pastEvents,futureEvents]

            #load into json
            temp_data = json.loads(str(knight.metric_cache))
            temp_data[key] = value

            #write back
            knight.metric_cache = json.dumps(temp_data)
            knight.save()

    def get_cached(self):
        knight=self.getDBObject()
        return json.loads(self.get('metric_cache'))
