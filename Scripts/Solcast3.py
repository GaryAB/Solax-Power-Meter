 

def getForecast(dayUsed):

    import requests
    import json
    import datetime
    import time

    solcastKey = 'ABCDEFGHIJKLMONPQRSTUVWXYZ123456' # obtain from Solcast website
    resourceID = 'XXXX-XXXX-XXXX-XXXX' # obtain from Solcast website
    capacity = 11.6 # Capacity of battery in kWh

    date = datetime.datetime.utcnow()
    dayNum = date.strftime("%j")
    nowTime = datetime.datetime.utcnow()
    localTime = datetime.datetime.now()
    timezone = int(nowTime.strftime("%H")) - int(nowTime.strftime("%H"))
        
    index = 0
    success = 0
    fail = 0
    while success == 0:
     try:
       surl = 'https://api.solcast.com.au/rooftop_sites/' + resourceID + '/forecasts?format=json&api_key=' + solcastKey
       x = requests.get(surl)
       # some JSON:
       x = (x.text)
       y = json.loads(x)
       success = 1
     except:
       fail = 1
       return "Unable to contact Solcast"
       time.sleep(300)

     try:
        total = 0
        result = (y["forecasts"])
        x = str(result)
        z = x.replace("'","\"")
        z = z.replace("None","null")
        # parse z:
        y = json.loads(z)
        # the result is a Python dictionary:
        while index < 54:
         result = (y[index])
         a = str(result)
         b = a.replace("'","\"")
         b = b.replace("None","null")
         c = json.loads(b)
         index = int(index + 1)
         result = c["period_end"]
         solYear = int(result[0:4])
         solMonth = int(result[5:7])
         solDay = int(result[8:10])
         solHour = int(result[11:13]) + timezone
         if solHour > 23:
            solHour = solHour - 24
         solMin = int(result[14:16])
         solDate = datetime.datetime(solYear, solMonth, solDay)
         solNum = solDate.strftime("%j")
         if (int(solNum) == int(dayNum) + 1) and (solHour < 15) or ((int(solNum) == int(dayNum) + 1) and (solHour == 15) and (solMin == 0)):
             total = total + c["pv_estimate"]
         solYield = total/2
        preload = int((capacity+dayUsed-solYield)*100 / capacity)
        if preload > 95:
         preload = 95
        if preload > 10:
         reply = ("Recommended preload for tonight is " + str(preload) + "%")
        else:
         reply = ("No recommended preload tonight")
        return reply
     except:
        success = 0
        return "Data invalid from Solcast"
        time.sleep(300)
