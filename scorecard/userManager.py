from .models import *
from django.core.exceptions import *
import time


class user():

    def __init__(self,gid):
        self.gid = gid

    #make - makes an entry that includes the details for that user (option to overwrite if already exists)
    def make(self,user_data):
        #make sure all of the data exists in user_data
        data_present = (user_data.get("gid") is not None)
        data_present = (user_data.get("access_token") is not None) and data_present
        data_present = (user_data.get("expires_at") is not None) and data_present
        data_present = (user_data.get("name") is not None) and data_present
        data_present = (user_data.get("email") is not None) and data_present

        if(not data_present):
            return False

        #create the user
        new_user = userInfo(gid=user_data["gid"], 
            access_token=user_data["access_token"], 
            expires_at=user_data["expires_at"],
            name=user_data["name"],
            email=user_data["email"])

        #save
        new_user.save()

        return True

    #exists - returns whether the user exists or not
    def exists(self):
        
        try:
            user = userInfo.objects.get(gid=self.gid)
        except userInfo.DoesNotExist as err:
            print(err)
            return False
        
        if(user != None):
            return True
        else:
            return False


    #delete - deletes the user

    #update_token - updates the access token and the experation date

    #is_expired - checks if the access token is expired
    def token_expired(self):
        user = userInfo.objects.get(gid=self.gid).dict()
        if( int(time.time()) > int(user["expires_at"])):
            return True
        else:
            return False

    #get_all - get all fields
    def get_all(self):
        try:
            user=userInfo.objects.get(gid=self.gid).dict()
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
        



class knight():
    
    def __init__(self,name):
        self.name = name

    #get_all - get all fields
    def get_all(self):
        try:
            knight=knightInfo.objects.get(name=self.name).dict()
            return knight
        except knightInfo.DoesNotExist as err:
            print(err)
            return None

    #get - get a specific field (returns None if it does not exist)
    def get(self,metric):
        knight_info = self.get_all()
        print(knight_info)

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
        
