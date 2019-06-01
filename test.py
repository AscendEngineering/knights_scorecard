import sys
import os
import datetime
from scorecard.models import *


def main(argv):

    newtime = formatTime(str(datetime.datetime.now()))

    formdata = {'client_name': 'hey', 'client_details': 'sadfsadf', 'date': '2019-05-05', 'time': '17:00'}

    

    postToCal(formdata)



if __name__ == '__main__':
    main(sys.argv)