from .models import *
from django.core.exceptions import *
import time


class site_user():

    def __init__(self,email):
        self.email = email

    #exists - returns whether the user exists or not
    def exists(self):
        
        try:
            user = userInfo.objects.get(email=self.email)
        except userInfo.DoesNotExist as err:
            print(err)
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
                print("metric does not exist")
                return None
        else:
            return None

        return retVal
        
    #user has logged on, increment log on number
    def loggedOn(self):
        
        try:
            user=userInfo.objects.get(email=self.email)
        except userInfo.DoesNotExist as err:
            print(err)
            return

        #increment log on
        new_timesLoggedIn = int(user.timesLoggedIn) +1
        userInfo.objects.filter(email=self.email).update(timesLoggedIn=new_timesLoggedIn)
        
        


class knight():
    
    def __init__(self,name):
        self.name = name

    #get_all - get all fields
    def get_all(self):
        try:
            #split into first and last
            firstname = self.name.split(' ')[0]
            lastname = self.name.split(' ')[1]
            knight=knightInfo.objects.all().filter(name__icontains=firstname).get(name__icontains=lastname).dict()
            return knight
        except knightInfo.DoesNotExist as err:  
            print(err)
            return None

    #get - get a specific field (returns None if it does not exist)
    def get(self,metric):
        knight_info = self.get_all()

        retVal = ""
        if(knight_info != None):
            try:
                retVal = knight_info[metric]
            except KeyError as err:
                print("metric does not exist")
                return None
        else:
            return None

        return retVal
        
