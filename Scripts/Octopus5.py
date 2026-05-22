def check():

  import requests
  import json
  import datetime
  import Settings
  import time

  global data
  global date
  region = Settings.region
  data = None
  date = None
  endTime = None
  startTime = ""
  
  id = 0

  try:

    localTime = datetime.datetime.now()
    date = (str(localTime)[0:10])
    url = 'https://api.neso.energy/api/3/action/datastore_search?resource_id=cc36fff5-5f6f-4fde-8932-c935d982ecd8'
    sessDate = date
    stop = 0
    stop1 = 0

    while (sessDate == date) and stop == 0:
      x = requests.post(url)
      x = (x.text)
      x = json.loads(x)
      y = x["success"]
      if y != True:
        return ("",0,0,0,0,0)
      y = x["result"]
      z = y["records"]
      del x
      id = 0
         
      while (id < 100) and (stop == 0):
        record = z[id]
        supplier = record["Registered DFS Participant"]
        sessDate = record["Delivery Date"]
        if (supplier != "OCTOPUS ENERGY LIMITED"):
          id = id + 1
          continue
        if sessDate != date:
          id = id + 1
          continue
        status = record["Status"]        
        if status != "Accepted":
          id = id + 1
          continue
        level = (record[region])
        if level == 0:
          id = id + 1
          continue
        
        if record["From"] != endTime:
          startTime = record["From"]
        endTime = record["To"]
        sessDate = record["Delivery Date"]
        status = record["Status"]
        startHour = int(startTime[0:2])
        startMins = int(startTime[3:5])
        startComp = (startHour * 60) + startMins - 10
        startData = startHour + (startMins * 256)
        endHour = int(endTime[0:2])
        endMins = int(endTime[3:5])
        stop = 0
        id = id +1

      id = 0  
      p = y["_links"]
      q = p["next"]
      url = "https://api.neso.energy" + q

    if startTime != "":
      return ("Saving session today " + startTime + " to " + endTime,startData,startHour,startMins,endHour,endMins)  
    else:
      return ("",0,0,0,0,0)

  except Exception as e:
    errlog(e + " in Octopus5.py")
    return ("",0,0,0,0,0)
