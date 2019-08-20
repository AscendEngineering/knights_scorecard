from .models import *
from django.core.exceptions import *
import time


class knight():

    def __init__(self,gid):
        self.gid = gid

    #make - makes an entry that includes the details for that knight(option to overwrite if already exists)
    def make(self,user_data):
        #make sure all of the data exists in user_data
        data_present = (user_data.get("gid") is not None)
        data_present = (user_data.get("access_token") is not None) and data_present
        data_present = (user_data.get("expires_at") is not None) and data_present
        data_present = (user_data.get("name") is not None) and data_present
        data_present = (user_data.get("email") is not None) and data_present

        if(not data_present):
            return False

        return True

        #create the knight  
        knightInfo(gid=data_present["gid"], 
            access_token=data_present["access_token"], 
            expires_at=data_present["expires_at"],
            name=data_present["name"],
            email=data_present["email"])

        #save
        knightInfo.save()


    #exists - returns whether the user exists or not
    def exists(self):
        
        try:
            user = knightInfo.objects.get(gid=self.gid)
        except knightInfo.DoesNotExist as err:
            return False
        
        if(user != None):
            return True
        else:
            return False


    #delete - deletes the knight

    #update_token - updates the access token and the experation date

    #is_expired - checks if the access token is expired
    def is_expired(self):
        user = knightInfo.objects.get(gid=self.gid)
        if( int(time.time()) > int(user["expires_at"])):
            return True
        else:
            return False

    #get_all - get all fields
    def get_all(self):
        try:
            user=knightInfo.objects.get(gid=self.gid)
            return user
        except:
            return None

    #get - get a specific field (returns None if it does not exist)
    def get(self,metric):
        user_info = self.get_all()

        if(user_info != None):
            return user_info.get(metric)
        else:
            return None
        
