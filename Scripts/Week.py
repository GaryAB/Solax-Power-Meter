def means(dayUse):
  import requests
  import json
  import datetime
  import time
  import os

  nowTime = datetime.datetime.utcnow()

  if os.path.exists("daymeans.json"):
    f = open("daymeans.json", "r")
    dataJson = f.read()
    data = json.loads(dataJson)
    meanDayUse = data[nowTime.strftime("%A")]
    if meanDayUse != 0:
     data[nowTime.strftime("%A")] = ((meanDayUse * 3) + dayUse)/4
    else:
     data[nowTime.strftime("%A")] = dayUse
  else:
     data = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0} 

  f = open("daymeans.json", "w")
  dataJson = json.dumps(data)
  f.write(dataJson)
  f.close
  tomTime = datetime.datetime.utcnow() + datetime.timedelta(days = 1)
  tomorrow = tomTime.strftime("%A")
  print (tomorrow)
  if data[tomorrow] > 0:
    return float(data[tomorrow])
  else:
    return 7
