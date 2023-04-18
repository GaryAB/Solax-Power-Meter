import requests
import json
import datetime
import time
import math
import os
import Solcast3
import Week

tokenID = '12345678912345678912' #API Token from Solax cloud website
inverterPassword = 'SXXXXXXXXX'  #Password to access inverter - get from Solax Cloud website
startCheapRate = 0  #Start of cheap rate electricty in hours (UTC)
endCheapRate = 7  #Start of full rate electricity in hours (UTC)
solcast = "OFF"  #Set to 'ON' if using Solcast to forecast overnight preload (see notes)

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
angle = (1000-2500)/2500*0.45

line = Line(Point(200+math.sin(angle)*400, 480-math.cos(angle)*400), Point(200+math.sin(angle)*360, 480-math.cos(angle)*360))
line.setWidth(1)
line.draw(win)

angle = (2000-2500)/2500*0.45

line = Line(Point(200+math.sin(angle)*400, 480-math.cos(angle)*400), Point(200+math.sin(angle)*360, 480-math.cos(angle)*360))
line.setWidth(1)
line.draw(win)

angle = (3000-2500)/2500*0.45

line = Line(Point(200+math.sin(angle)*400, 480-math.cos(angle)*400), Point(200+math.sin(angle)*360, 480-math.cos(angle)*360))
line.setWidth(1)
line.draw(win)

angle = (4000-2500)/2500*0.45

line = Line(Point(200+math.sin(angle)*400, 480-math.cos(angle)*400), Point(200+math.sin(angle)*360, 480-math.cos(angle)*360))
line.setWidth(1)
line.draw(win)

text = Text(Point(200,35),'PV power')
text.draw(win)

#Draw labels
text = Text(Point(495,35),'Battery State of Charge')
text.draw(win)

text = Text(Point(660,35),'Grid use today*')
text.draw(win)

text = Text(Point(660,300),'*while app running ')
text.draw(win)

text = Text(Point(80,82),'1kW')
text.draw(win)

text = Text(Point(160,70),'2kW')
text.draw(win)

text = Text(Point(240,70),'3kW')
text.draw(win)

text = Text(Point(320,82),'4kW')
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
oldangle = -0.45
oldfeedangle = -0.45
oldbatangle = -0.45
nightGood = 0
dayGood = 0
oldNightUsed = 0
oldDayUsed = 0
messageErased = 0
oldFeedIn = 0
solDone = 0
usedFailed = 1
startDayUsed = 0
endDayUsed = 0
todayUsed = 7

# make conditional
if os.path.exists("power.json"):
  f = open("power.json", "r")
  dataJson = f.read()
  data = json.loads(dataJson)
  nightStart = data["nightStart"]
  nightUsed = data["nightUsed"]
  dayStart = data["dayStart"]
  dayUsed = data["dayUsed"]
  startDayUsed = data["startDayUsed"]
  endDayUsed = data["endDayUsed"]
  todayUsed = data["todayUsed"]
  if nightStart > 0:
    nightGood = 1
  if dayStart > 0:
    dayGood = 1  
else:
  nightStart = 0
  nightUsed = 0
  dayStart = 0 
  dayUsed = 0

while t < 2000000:
 success = 0
 fail = 0
 while success == 0:
  try:
   url = 'https://www.solaxcloud.com/proxyApp/proxy/api/getRealtimeInfo.do?tokenId=' + tokenID + '&sn=' + inverterPassword
   x = requests.get(url)
   x = (x.text)
   y = json.loads(x)
  except:
   rect = Rectangle(Point(0,350), Point(800,400))
   rect.setFill("Light Gray")
   rect.setOutline('Light Gray')
   rect.draw(win)
   text = Text(Point(400,370),"Unable to contact cloud")
   text._reconfig("font",("Arial",24,"bold"))
   text.setFill("Red")
   text.draw(win)
  
   fail = 1
   time.sleep(300)
   messageErased = 0
   continue
  if str(y["success"]) == "True":
   success = 1
  else:
   fail = fail + 1
   if fail >= 6:
    rect = Rectangle(Point(0,350), Point(800,400))
    rect.setFill("Light Gray")
    rect.setOutline('Light Gray')
    rect.draw(win)
    text = Text(Point(400,370),"Too many failures contacting cloud")
    text._reconfig("font",("Arial",24,"bold"))
    text.setFill("Red")
    text.draw(win)
    time.sleep(300)
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

  angle = (int(total)-2500)/2500*0.45
  feedangle = (int(y['feedinpower'])-2500)/2500*0.45
  batangle = (-int(y['batPower'])-2500)/2500*0.45

# clear pointers if relevant
  if angle != oldangle:
   unpointer = Line(Point(200+math.sin(oldangle)*200, 480-math.cos(oldangle)*200), Point(200+math.sin(oldangle)*360, 480-math.cos(oldangle)*360))
   unpointer.setOutline("yellow")
   unpointer.setWidth(8)
   unpointer.draw(win)
  
  if (feedangle != oldfeedangle) and (oldfeedangle >= -0.45):
   unfeedpointer = Line(Point(200+math.sin(oldfeedangle)*200, 480-math.cos(oldfeedangle)*200), Point(200+math.sin(oldfeedangle)*360, 480-math.cos(oldfeedangle)*360))
   unfeedpointer.setOutline("yellow")
   unfeedpointer.setWidth(8)
   unfeedpointer.draw(win)
   
  if (batangle != oldbatangle) and (oldbatangle >= -0.45):
   unbatpointer = Line(Point(200+math.sin(oldbatangle)*200, 480-math.cos(oldbatangle)*200), Point(200+math.sin(oldbatangle)*360, 480-math.cos(oldbatangle)*360))
   unbatpointer.setOutline("yellow")
   unbatpointer.setWidth(8)
   unbatpointer.draw(win)
  

# create pointer for battery power
  if float(y['batPower']) < 0:
    bat = 1
  
    batpointer = Line(Point(200+math.sin(batangle)*200, 480-math.cos(batangle)*200), Point(200+math.sin(batangle)*360, 480-math.cos(batangle)*360))
    batpointer.setOutline("Blue")
    batpointer.setWidth(8)
    batpointer.draw(win)

    text = Text(Point(200,320),'Battery power')
    text.setOutline("Blue")
    text.draw(win)
  
# create pointer for feed to grid
  elif float(y['feedinpower']) > 0:
    feed = 1
  
    feedpointer = Line(Point(200+math.sin(feedangle)*200, 480-math.cos(feedangle)*200), Point(200+math.sin(feedangle)*360, 480-math.cos(feedangle)*360))
    feedpointer.setOutline("Red")
    feedpointer.setWidth(8)
    feedpointer.draw(win)

    text = Text(Point(200,320),'Power to grid')
    text.setOutline("Red")
    text.draw(win)
  else:
    #remove text
    rect = Rectangle(Point(0,305), Point(400,350))
    rect.setFill("Light Gray")
    rect.setOutline('Light Gray')
    rect.draw(win)

# create pointer for PV Power
  pointer = Line(Point(200+math.sin(angle)*200, 480-math.cos(angle)*200), Point(200+math.sin(angle)*360, 480-math.cos(angle)*360))
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

  if (float(y['feedinpower']) < 1) and (feed == 1):
    feed = 0 

  oldfeedangle = feedangle
  
  oldbatangle = batangle

  oldangle = angle

  nowTime = datetime.datetime.utcnow()
  localTime = datetime.datetime.now()
  if (int(nowTime.strftime("%H")) == 0) and (int(nowTime.strftime("%M")) == 0):
    nightStart = float(y["consumeenergy"])
    nightGood = 1
    solDone = 0
    usedFailed = 1

  # erase preload message
  if (int(localTime.strftime("%H")) == 1) and (int(localTime.strftime("%M")) == 0):
    rect = Rectangle(Point(0,350), Point(800,400))
    rect.setFill("Light Gray")
    rect.setOutline('Light Gray')
    rect.draw(win)

    
  if (int(nowTime.strftime("%H")) == 7) and (int(nowTime.strftime("%M")) == 0):
    dayStart = float(y["consumeenergy"])
    dayGood = 1
    startDayUsed = float(y["consumeenergy"]) + float(y["yieldtotal"]) - float(y["feedinenergy"])
    usedFailed = 2

  if (int(nowTime.strftime("%H")) == 15) and (int(nowTime.strftime("%M")) == 0):
    endDayUsed = float(y["consumeenergy"]) + float(y["yieldtotal"]) - float(y["feedinenergy"])
    todayUsed = endDayUsed - startDayUsed
    todayUsed = Week.means(todayUsed)
    if usedFailed == 2:
      usedFailed = 0


  if solcast == 'ON':
    if (int(localTime.strftime("%H")) >= 21) and (solDone != 1):
      if usedFailed == 0: 
        text = Text(Point(400,370), Solcast3.getForecast(todayUsed))
      else:
        text = Text(Point(400,370), Solcast3.getForecast(7)) 
      text._reconfig("font",("Arial",24,"bold"))
      text.setFill("Blue")
      text.draw(win)
      solDone = 1
    
     
  if nightGood == 1:
    if (int(nowTime.strftime("%H")) >= startCheapRate and int(nowTime.strftime("%H")) < endCheapRate):
        nightUsed = int((y["consumeenergy"] - nightStart)*100)/100
    else:
        nightUsed = localData["nightUsed"]    
    if oldNightUsed != nightUsed:
      rect = Rectangle(Point(600,240 ), Point(800,260))
      rect.setFill("Light Gray")
      rect.setOutline('Light Gray')
      rect.draw(win)
      text = Text(Point(660,250), str(nightUsed) + " kWh")
      text._reconfig("font",("Arial",18,"normal"))
      text.draw(win)
      oldNightUsed = nightUsed
    if (int(nowTime.strftime("%H")) >= 7):
      nightGood = 0
    
  if dayGood == 1:
    if not(int(nowTime.strftime("%H")) >= startCheapRate and int(nowTime.strftime("%H")) < endCheapRate):
        dayUsed =int((["consumeenergy"] - dayStart)*100)/100
    else:
        dayUsed = localData["dayUsed"]
    if oldDayUsed != dayUsed:
      rect = Rectangle(Point(600,140 ), Point(800,160))
      rect.setFill("Light Gray")
      rect.setOutline('Light Gray')
      rect.draw(win)
      text = Text(Point(660,150), str(dayUsed) + " kWh")
      text._reconfig("font",("Arial",18,"normal"))
      text.draw(win)
      oldDayUsed = dayUsed
    if (int(nowTime.strftime("%H")) < 7):
      dayGood = 0                                                

#Save data
  if float(y['feedinpower']) != oldFeedIn: 
    data = {"nightStart": nightStart, "nightUsed": nightUsed, "dayStart": dayStart, "dayUsed": dayUsed, "startDayUsed": startDayUsed, "endDayUsed": endDayUsed, "todayUsed": todayUsed}
    dataJson = json.dumps(data)

    f = open("power.json", "w")
    f.write(dataJson)
    f.close()
    oldFeedIn = y['feedinpower']

  if float(y['feedinpower']) > 2500:
    charge = 1
  if (float(y['feedinpower']) < 0) and (charge == 1):
    charge = 0 
  time.sleep(30)
  t = t + 1 
