

import requests
import json
import datetime
import re
import Settings

def find():

    try:
        # set current date and time  
        localTime = datetime.datetime.now()
        if Settings.timeZone.upper() == "UTC":
            nowTime= datetime.datetime.utcnow()
        else:
            nowTime = localTime

        #set months
        year = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        s = requests.Session()
        url = 'https://octopus.energy/free-electricity/'

        # scan website
        x = requests.get(url)
        x = (x.text)
        y = re.search("Next Free electricity session:",x)
        y = (y.span())
        y = y[1]
        x = x[y+4:y+50]
        z = re.search("<",x)
        z = (z.span())
        z = z[0]
        text = "Saving Session " + (x[0:z])
        a = 0
        month = 0
        pm = 0

        # find month
        while a < 12:
            b = re.search(year[a],x)
            if b != None:
                month = a+1
                break
            a = a + 1
        if month == 0:
            text = ""

        # find am or pm
        a = re.search("am",x)
        if a == None:
            pm = 1

        # fimd date and time
        a = 0
        i = 0
        time = [0,0,0,0,0,0]
        while i < z:
            a = re.search ("\d",x)
            if a == None:
                break
            a = (a.span())
            b = a[0]
            if b == 0:
                time[i-1] = (time[i-1] * 10) + int(x[b])
            else:
                time[i] = int(x[b])
                i = i + 1
                if i == 2:
                    timeText = x
            x = x[(b+1):z]
            if x[0] == "-":
                i = 3
        date = time[0]
        startHr = time[1]
        startMin = time[2]
        endHr = time[3]
        endMin = time[4]

        a = re.search ("\d",timeText)
        a = (a.span())
        a = a[0]
        timeText = timeText[a:]   
        
        # Convert to 24 hour clock
        if pm == 1:
            startHr = startHr + 12
        if endHr < startHr:
            endHr = endHr + 12

        # check if returned date is in the past.
        if (int(localTime.strftime("%d")) > date) or (int(localTime.strftime("%m")) > month):
            text = ''                                            
               
        return (text, month, date, startHr, startMin, endHr, endMin, timeText)
    except:
        return ("", 0, 0, 0, 0, 0, 0, "")
