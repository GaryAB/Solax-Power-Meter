def logPower(dayGrid,nightGrid,solarYield,batteryUse,export):
  import datetime
  import time
  import os

  complete = 0

  solarYield = int(solarYield*100)/100
  batteryUse = int(batteryUse*100)/100
  export = int(export*100)/100

  localTime = datetime.datetime.now()
  if (int(localTime.strftime("%H"))) < 12:
    dayBack = localTime - datetime.timedelta(days = 1)
    logDate = dayBack.strftime("%d/%m/%Y")
  else:
    logDate = localTime.strftime("%d/%m/%Y")
  if os.path.exists("powerlog.csv"):
    line = logDate + "," + str(solarYield) + "," + str(batteryUse) + "," + str(dayGrid) +"," + str(nightGrid) + "," +str(export) + "\r"
    complete = 1
  else:
    line = "Date,Solar Yield, Battery use, Peak Grid use, Off-peak Grid Use,Power to Grid" + "\r"
    complete = 0

  f = open("powerlog.csv","a")
  f.write(line)
  f.close()
  return complete
