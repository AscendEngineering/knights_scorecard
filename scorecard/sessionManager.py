

import scorecard.klogging as LOG

class session():
    def __init__(self,request):
        self.request = request

    #get an attribute
    def get(self,key):
        try:
            value = self.request.session.__getitem__(key)
            return value

        except KeyError as err:
            LOG.error("Error finding user session value",key)
            return None


    #set an attribute (return bool)
    def set(self,key,value):
        try:
            self.request.session.__setitem__(key,value)
        except:
            return False

        return True

    #delete an attribute (return bool)
    def delete(self,key):
        try:
            self.request.session.__delitem__(key)
        except KeyError as err:
            LOG.error("Key does not exist in session")
            return False
        
        return True