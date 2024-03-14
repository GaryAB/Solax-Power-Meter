import Settings
import requests
import json
import datetime
import time
import math
import os
import Solcast4
import Week2
import powerLog

def display(message,color):
  rect = Rectangle(Point(0,350), Point(800,400))
  rect.setFill("Light Gray")
  rect.setOutline('Light Gray')
  rect.draw(win)
  text = Text(Point(400,370),message)
  text._reconfig("font",("Arial",24,"bold"))
  text.setFill(color)
  text.draw(win)

# set current date and time
localTime = datetime.datetime.now()
if Settings.timeZone.upper() == "UTC":
  nowTime = datetime.datetime.utcnow()
else:
  nowTime = localTime
currentDate = int(localTime.strftime("%d"))

#Create look-up tables
pangle = -0.45
pointstartx = [200+math.sin(pangle)*200]
pointstarty = [480-math.cos(pangle)*200]
pointendx = [200+math.sin(pangle)*360]
pointendy = [480-math.cos(pangle)*360]
a = 1
while a <= Settings.scale*10:
  pangle = (int(a*100)-(Settings.scale * 500))/(Settings.scale*500)*0.45
  pointstartx.append(200+math.sin(pangle)*200)
  pointstarty.append(480-math.cos(pangle)*200)
  pointendx.append(200+math.sin(pangle)*360)
  pointendy.append(480-math.cos(pangle)*360)
  a = a + 1
   
from graphics import *
win = GraphWin("Solar Power Meter",800,480)

rect = Rectangle(Point(0,0), Point(800,480))
rect.setFill('light gray')
rect.draw(win)

head = Circle(Point(200,480), 400) # set center and radius
head.setFill("yellow")
head.draw(win)

head = Circle(Point(200,480), 199) # set center and radius
head.setFill("light grey")
head.draw(win)

rect = Rectangle(Point(400, 0), Point(800,480))
rect.setFill("light grey")
rect.setOutline('light gray')
rect.draw(win)

# Get and draw three vertices of triangle
p1 = Point(0,80)
p1.draw(win)
p2 = Point(0,480)
p2.draw(win)
p3 = Point(200,480)
p3.draw(win)
vertices = [p1, p2, p3]

# Use Polygon object to draw the triangle
triangle = Polygon(vertices)
triangle.setFill('light gray')
triangle.setOutline('light gray')
triangle.setWidth(0)  # width of boundary line
triangle.draw(win)

# Get and draw three vertices of triangle
p1 = Point(400,80)
p1.draw(win)
p2 = Point(400,480)
p2.draw(win)
p3 = Point(200,480)
p3.draw(win)
vertices = [p1, p2, p3]

# Use Polygon object to draw the triangle
triangle = Polygon(vertices)
triangle.setFill('light gray')
triangle.setOutline('light gray')
triangle.setWidth(0)  # width of boundary line
triangle.draw(win) 


#Draw graduations
cal = 1
while cal < Settings.scale:
  angle = ((cal*1000)-(Settings.scale*500))/(Settings.scale*500)*0.45

  line = Line(Point(200+math.sin(angle)*400, 480-math.cos(angle)*400), Point(200+math.sin(angle)*360, 480-math.cos(angle)*360))
  line.setWidth(1)
  line.draw(win)
  text = Text(Point(200+math.sin(angle)*410,480-math.cos(angle)*410),str(cal))
  text.draw(win)
  cal = cal + 1

text = Text(Point(200,35),'PV power (kW)')
text.draw(win)

#Draw labels
text = Text(Point(495,35),'Battery State of Charge')
text.draw(win)

text = Text(Point(660,35),'Grid use today*')
text.draw(win)

text = Text(Point(660,300),'*while app running ')
text.draw(win)

#Draw battery
rect = Rectangle(Point(450, 100), Point(540,300))
rect.setFill("White")
rect.setWidth(3)
rect.setOutline('Black')
rect.draw(win)

rect = Rectangle(Point(480, 80), Point(510,100))
rect.setFill("Red")
rect.setOutline('Black')
rect.draw(win)

#Draw sun
sun = Circle(Point(660,100), 10) # set center and radius
sun.setFill("yellow")
sun.setOutline('Yellow')
sun.draw(win)

line = Line(Point(660,80), Point(660,120))
line.setWidth(3)
line.setOutline('Yellow')
line.draw(win)

line = Line(Point(646,86), Point(674,114))
line.setWidth(3)
line.setOutline('Yellow')
line.draw(win)

line = Line(Point(640,100), Point(680,100))
line.setWidth(3)
line.setOutline('Yellow')
line.draw(win)

line = Line(Point(646,114), Point(674,86))
line.setWidth(3)
line.setOutline('Yellow')
line.draw(win)

#Draw Moon
moon = Circle(Point(660,200), 10) # set center and radius
moon.setFill("White")
moon.setOutline('White')
moon.draw(win)

moon = Circle(Point(665,200), 8) # set center and radius
moon.setFill("Light Gray")
moon.setOutline('Light Gray')
moon.draw(win)

t = 0
charge = 0
feed = 0
y = {}
mode = 'none'
oldfeedpower = 0
oldbatpower  = 0
oldtotal = 0
chargepower = 0
oldcharge = 0
nightGood = 0
dayGood = 0
oldNightUsed = 0
lastNightUsed = 0
oldDayUsed = 0
messageErased = 0
oldFeedIn = 0
solDone = 0
usedFailed = 1
startDayUsed = 0
endDayUsed = 0
todayUsed = 7
pMessage = None
noFile = 0
solarYield = 0
batteryUse = 0
Settings.logDone = 1
export = 0
feedinenergy = 0
oldFeedEnergy = 0
firstPass = 0
if Settings.startCheapRate < 12:
  Settings.startCheapRate = (Settings.startCheapRate + 12) * 60 + Settings.crMins
else:
  Settings.startCheapRate = (Settings.startCheapRate - 12) * 60 + Settings.crMins
if Settings.endCheapRate < 12:
  Settings.endCheapRate = (Settings.endCheapRate + 12) * 60 + Settings.prMins
else:
  Settings.endCheapRate = (Settings.endCheapRate - 12) * 60 + Settings.prMins
  

# make conditional
if os.path.exists("power.json"):
  f = open("power.json", "r")
  localDataJson = f.read()
  localData = json.loads(localDataJson)
  recordDate = localData["Date"]
  if currentDate == recordDate:
    dateError = 0
    setDate = recordDate
    nightStart = localData["nightStart"]
    nightUsed = localData["nightUsed"]
    lastNightUsed = nightUsed
    dayStart = localData["dayStart"]
    dayUsed = localData["dayUsed"]
    startDayUsed = localData["startDayUsed"]
    endDayUsed = localData["endDayUsed"]
    todayUsed = localData["todayUsed"]
    solarYield = localData["solarYield"]
    batteryUse = localData["batteryUse"]
    export = localData["export"]
    if nightStart > 0:
      nightGood = 1
    if dayStart > 0:
      dayGood = 1  
  else:
    setDate = currentDate
    dateError = 1
    nightStart = 0
    nightUsed = 0
    dayStart = 0 
    dayUsed = 0
    solarYield = 0
    batteryUse = 0
    export = 0 
else:
  setDate = currentDate
  dateError = 1
  nightStart = 0
  nightUsed = 0
  dayStart = 0 
  dayUsed = 0
  noFile = 1
  solarYield = 0
  batteryUse = 0
  export = 0 
  
while True:
 success = 0
 fail = 0
 currentDate = int(localTime.strftime("%d"))
 while success == 0:
  try:
   url = 'https://www.solaxcloud.com/proxyApp/proxy/api/getRealtimeInfo.do?tokenId=' + Settings.tokenID + '&sn=' + Settings.inverterPassword
   x = requests.get(url)
   x = (x.text)
   y = json.loads(x)
  except:
   display("Unable to contact cloud","red")  
   fail = 1
   time.sleep(300)
   messageErased = 0
   continue
  if str(y["success"]) == "True":
   success = 1
  else:
   fail = fail + 1
   if fail >= 6:
     display("Too many failures contacting cloud","red")
     time.sleep(300) 

   if pMessage != None:
     display(pMessage,"blue")
   else:
     messageErased = 0
   continue
  
 if success == 1:
  if messageErased != 1:
    rect = Rectangle(Point(0,350), Point(800,400))
    rect.setFill("Light Gray")
    rect.setOutline('Light Gray')
    rect.draw(win)
    messageErased = 1
    solDone = 0
  result = (y["result"])
  x = str(result)
  z = x.replace("'","\"")
  z = z.replace("None","null")
  # parse x:
  y = json.loads(z)
  # the result is a Python dictionary:
  total = (y['powerdc1'])+(y['powerdc2'])
  q = datetime.datetime.now()
  ntime = str(q.strftime("%X"))

  feedpower = int(y['feedinpower'])
  batpower = -int(y['batPower'])
  if batpower < 0:
    chargepower = -batpower
    batpower = 0
  else:
    chargepower = 0

  
  oldmode = mode

# create pointer for charge power
  if (chargepower > 0) and (chargepower > feedpower):
    if chargepower > (Settings.scale*1000):
      chargepower = Settings.scale*1000
    mode = 'charge'
    pcchargepower = chargepower/100
  

# create pointer for battery power
  elif batpower > 0:
    if batpower > (Settings.scale*1000):
      batpower = Settings.scale*1000
    mode = 'bat'
    pcbatpower = batpower/100
  
  
# create pointer for feed to grid
  elif (feedpower > 0) and (feedpower > chargepower):
    if feedpower > (Settings.scale*1000):
      feedpower = Settings.scale*1000
    mode = 'feed'
    pcfeedpower = feedpower/100

  else:
    mode = 'none'

# clear pointers if relevant
  if int(total/100) != int(oldtotal/100):
   pcoldtotal = oldtotal/100 
   unpointer = Line(Point(pointstartx[int(pcoldtotal)], pointstarty[int(pcoldtotal)]), Point(pointendx[int(pcoldtotal)], pointendy[int(pcoldtotal)]))
   unpointer.setOutline("yellow")
   unpointer.setWidth(8)
   unpointer.draw(win)
  
  if ((int(chargepower/100) != int(oldcharge/100)) and (int(oldcharge/100) >= 0)) or (chargepower == 0) or (feedpower > chargepower):
   pcoldcharge = oldcharge/100
   unchargepointer = Line(Point(pointstartx[int(pcoldcharge)], pointstarty[int(pcoldcharge)]), Point(pointendx[int(pcoldcharge)], pointendy[int(pcoldcharge)]))
   unchargepointer.setOutline("yellow")
   unchargepointer.setWidth(8)
   unchargepointer.draw(win)
   
  if ((int(feedpower/100) != int(oldfeedpower/100)) and (int(oldfeedpower/100) >= 0)) or (feedpower == 0):
   pcoldfeedpower = oldfeedpower/100
   unfeedpointer = Line(Point(pointstartx[int(pcoldfeedpower)], pointstarty[int(pcoldfeedpower)]), Point(pointendx[int(pcoldfeedpower)], pointendy[int(pcoldfeedpower)]))
   unfeedpointer.setOutline("yellow")
   unfeedpointer.setWidth(8)
   unfeedpointer.draw(win)
   
  if ((int(batpower/100) != int(oldbatpower/100)) and (int(oldbatpower/100) >= 0)) or (batpower == 0):
   pcoldbatpower = oldbatpower/100
   unbatpointer = Line(Point(pointstartx[int(pcoldbatpower)], pointstarty[int(pcoldbatpower)]), Point(pointendx[int(pcoldbatpower)], pointendy[int(pcoldbatpower)]))
   unbatpointer.setOutline("yellow")
   unbatpointer.setWidth(8)
   unbatpointer.draw(win)


#write pointer for charge power
  if mode == 'charge':
    chargepointer = Line(Point(pointstartx[int(pcchargepower)], pointstarty[int(pcchargepower)]), Point(pointendx[int(pcchargepower)], pointendy[int(pcchargepower)]))
    chargepointer.setOutline("Green")
    chargepointer.setWidth(8)
    chargepointer.draw(win)

#write pointer for battery power
  if mode == 'bat':
    batpointer = Line(Point(pointstartx[int(pcbatpower)], pointstarty[int(pcbatpower)]), Point(pointendx[int(pcbatpower)], pointendy[int(pcbatpower)]))
    batpointer.setOutline("Blue")
    batpointer.setWidth(8)
    batpointer.draw(win)

#write pointer for feed to grid
  if mode == 'feed':
    feedpointer = Line(Point(pointstartx[int(pcfeedpower)], pointstarty[int(pcfeedpower)]), Point(pointendx[int(pcfeedpower)], pointendy[int(pcfeedpower)]))
    feedpointer.setOutline("Red")
    feedpointer.setWidth(8)
    feedpointer.draw(win)



  if mode != oldmode:
    #remove text
    rect = Rectangle(Point(0,305), Point(400,350))
    rect.setFill("Light Gray")
    rect.setOutline('Light Gray')
    rect.draw(win)

  if mode == 'bat':
    text = Text(Point(200,320),'Battery power')
    text.setOutline("Blue")
    text.draw(win)
  elif mode == 'feed':
    text = Text(Point(200,320),'Power to grid')
    text.setOutline("Red")
    text.draw(win)
  elif mode == 'charge':
    text = Text(Point(200,320),'Charging')
    text.setOutline("Green")
    text.draw(win)

# create pointer for PV Power
  if total > (Settings.scale*1000):
    total = Settings.scale*1000
  pctotal = total/100

# draw pointer for PV power
  pointer = Line(Point(pointstartx[int(pctotal)], pointstarty[int(pctotal)]), Point(pointendx[int(pctotal)], pointendy[int(pctotal)]))
  pointer.setOutline("Black")
  pointer.setWidth(8)
  pointer.draw(win)

# display state of charge
  rect = Rectangle(Point(450, 100), Point(540,300-(y["soc"]*2)))
  rect.setFill("White")
  rect.setOutline('Black')
  rect.draw(win)

  rect = Rectangle(Point(450,300-(y["soc"]*2)), Point(540,300))
  rect.setFill("Blue")
  rect.setOutline('Blue')
  rect.draw(win)

# accumulate solar radiation total
  solarYield = solarYield + (total/120000)
# accumulate battery outpout total
  batteryUse = batteryUse + (batpower/120000)
# accumulate export power
  export = export + feedinenergy - oldFeedEnergy

  if (float(y['feedinpower']) < 1) and (feed == 1):
    feed = 0 

  oldfeedpower = feedpower
  oldbatpower = batpower
  oldtotal = total
  oldcharge = chargepower

  if y["feedinenergy"] != 0:
    oldFeedEnergy = feedinenergy
  else:
    oldFeedEnergy = 0

  feedinenergy = float(y["feedinenergy"])

  if firstPass == 0: 
    oldFeedEnergy = feedinenergy
    firstPass = 1

  # settimes
  localTime = datetime.datetime.now()
  if Settings.timeZone.upper() == "UTC":
    nowTime = datetime.datetime.utcnow()
  else:
    nowTime = localTime

  # set current time to time in minutes
  plusTime = nowTime + datetime.timedelta(hours = 12)
  nowTimeMins = ((int(plusTime.strftime("%H"))) * 60) + int(nowTime.strftime("%M"))

  if nowTimeMins == Settings.startCheapRate:
    nightStart = float(y["consumeenergy"])
    nightGood = 1
    noFile = 0
    solDone = 0
    usedFailed = 1

  # erase preload message
  if (int(localTime.strftime("%H")) == 1) and (int(localTime.strftime("%M")) == 0):
    rect = Rectangle(Point(0,350), Point(800,400))
    rect.setFill("Light Gray")
    rect.setOutline('Light Gray')
    rect.draw(win)
    pMessage = None
 
  if nowTimeMins == Settings.endCheapRate:
    currentDate = int(localTime.strftime("%d"))
    setDate = currentDate #only update date at start of daytime period
    dateError = 0
    dayStart = float(y["consumeenergy"])
    dayGood = 1
    startDayUsed = float(y["consumeenergy"]) + float(y["yieldtotal"]) - float(y["feedinenergy"])
    usedFailed = 2
    lastNightUsed = nightUsed

  if (int(localTime.strftime("%H")) == 15) and (int(localTime.strftime("%M")) == 0):
    endDayUsed = float(y["consumeenergy"]) + float(y["yieldtotal"]) - float(y["feedinenergy"])
    todayUsed = endDayUsed - startDayUsed
    Settings.logDone = 0
    noFile = 0
    if dateError == 0:
      todayUsed = Week2.means(todayUsed)
    if usedFailed == 2:
      usedFailed = 0

  if Settings.solcast.upper() == 'ON':
    if (int(localTime.strftime("%H")) >= 21) and (solDone != 1):
      if usedFailed == 0: 
        preload = Solcast4.getForecast(todayUsed)
      else:
        preload = Solcast4.getForecast(7)
      if type(preload) == str:
        pMessage = preload
      else:
        if preload > 95:
          preload = 95
        if preload > 10:
          pMessage = "Recommended preload for tonight is " + str(preload) + "%"
        else:
          preload = 10
          pMessage = "No recommended preload tonight"
        solDone = 1
      display(pMessage,"blue")

  if noFile == 0:
    if nightGood == 1:
      if (nowTimeMins >= Settings.startCheapRate) and (nowTimeMins < Settings.endCheapRate):
        nightUsed = int((y["consumeenergy"] - nightStart)*100)/100
      else:
        nightGood = 0     
      if oldNightUsed != nightUsed:
        rect = Rectangle(Point(600,240 ), Point(800,260))
        rect.setFill("Light Gray")
        rect.setOutline('Light Gray')
        rect.draw(win)
        text = Text(Point(660,250), str(nightUsed) + " kWh")
        text._reconfig("font",("Arial",18,"normal"))
        text.draw(win)
        oldNightUsed = nightUsed
      
    if dayGood == 1:
      if not((nowTimeMins >= Settings.startCheapRate) and (nowTimeMins < Settings.endCheapRate)):
          dayUsed = int((y["consumeenergy"] - dayStart)*100)/100
      else:
        dayGood = 0                                                
      if oldDayUsed != dayUsed:
        rect = Rectangle(Point(600,140 ), Point(800,160))
        rect.setFill("Light Gray")
        rect.setOutline('Light Gray')
        rect.draw(win)
        text = Text(Point(660,150), str(dayUsed) + " kWh")
        text._reconfig("font",("Arial",18,"normal"))
        text.draw(win)
        oldDayUsed = dayUsed

#Save data
  if (float(y['feedinpower']) != oldFeedIn) and (dateError == 0): 
    data = {"Date": setDate, "nightStart": nightStart, "nightUsed": nightUsed, "dayStart": dayStart, "dayUsed": dayUsed, "startDayUsed": startDayUsed, "endDayUsed": endDayUsed, "todayUsed": todayUsed, "solarYield": solarYield, "batteryUse": batteryUse, "export": export}
    dataJson = json.dumps(data)

    f = open("power.json", "w")
    f.write(dataJson)
    f.close()
    oldFeedIn = float(y['feedinpower'])

  oldtotal = total

  if feedpower < 0:
    feedpower = 0

  # Send data to Settings.log  
  if (Settings.log.upper() == "YES") and (Settings.logDone == 0) and (nowTimeMins >= Settings.startCheapRate):
    Settings.logDone = powerSettings.log.Settings.logPower(dayUsed,lastNightUsed,solarYield,batteryUse,export)
    if Settings.logDone == 1:
      solarYield = 0
      batteryUse = 0
      export = 0  


  if float(y['feedinpower']) > 2500:
    charge = 1
  if (float(y['feedinpower']) < 0) and (charge == 1):
    charge = 0 

  period = 30 - int(nowTime.strftime("%S"))
  if period <= 0:
    period = period + 30
  time.sleep(period)

