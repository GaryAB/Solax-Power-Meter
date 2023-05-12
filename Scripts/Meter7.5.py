import requests
import json
import datetime
import time
import math
import os
import Solcast4
import Week
import re
import scan
import set

scale = 5                         #scale of meter in kW
inverterAddress = 'dchp'          #address of inverter - use '5.8.8.8' if logged into inverter's access point
                                  #if the address is not static,  enter 'dchp'
                                  #Set DCHP range of your router on the lines below
From = '192.168.1.1'              #Start of address range for DCHP allocation
To = '192.168.1.254'              #End of address range for DCHP allocation
inverterPassword = 'SXKRR7EZR2'   #password to access inverter - found from SolaX Cloud website
startCheapRate = 0                #Start of cheap rate electricty in hours (UTC)
endCheapRate = 7                  #Start of full rate electricity in hours (UTC)
solcast = "ON"                    #Set to "ON" if using Solcast to forecast overnight preload (see Manual)
preloadSet = "AUTO"               #Set to "AUTO" to allow app to automatically set the overnight charging limit.
offset = 10                       #percentage offset added to recommended preload

def display(message,colour):
  rect = Rectangle(Point(0,350), Point(800,400))
  rect.setFill("Light Gray")
  rect.setOutline('Light Gray')
  rect.draw(win)
  text = Text(Point(400,370),message)
  text._reconfig("font",("Arial",24,"bold"))
  text.setFill(colour)
  text.draw(win)

#Create look-up tables
pangle = -0.45
pointstartx = [200+math.sin(pangle)*200]
pointstarty = [480-math.cos(pangle)*200]
pointendx = [200+math.sin(pangle)*360]
pointendy = [480-math.cos(pangle)*360]
a = 0
while a <= scale*10:
  pangle = (int(a*100)-(scale * 500))/(scale*500)*0.45
  pointstartx.append(200+math.sin(pangle)*200)
  pointstarty.append(480-math.cos(pangle)*200)
  pointendx.append(200+math.sin(pangle)*360)
  pointendy.append(480-math.cos(pangle)*360)
  a = a + 1

from graphics import *
win = GraphWin("Solar Power Meter",800,480)

#from colorama import init, Fore, Back, Style

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
while cal < scale:
  angle = ((cal*1000)-(scale*500))/(scale*500)*0.45

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
dchp = 0
pMessage = None

if inverterAddress.upper() == 'DCHP':
  dchp = 1
  inverterAddress = scan.ipScan(From, To, inverterPassword)
  if inverterAddress == None:
    text = Text(Point(400,370),"Inverter not found")
    text._reconfig("font",("Arial",24,"bold"))
    text.setFill("Red")
    text.draw(win)
    time.sleep(300)
    messageErased = 0
  else:
    inverterAddress = 'http://' + inverterAddress
else:
  inverterAddress = 'http://' + inverterAddress
# make conditional
if os.path.exists("power.json"):
  f = open("power.json", "r")
  localDataJson = f.read()
  localData = json.loads(localDataJson)
  nightStart = localData["nightStart"]
  nightUsed = localData["nightUsed"]
  dayStart = localData["dayStart"]
  dayUsed = localData["dayUsed"]
  startDayUsed = localData["startDayUsed"]
  endDayUsed = localData["endDayUsed"]
  todayUsed = localData["todayUsed"]
  if nightStart > 0:
    nightGood = 1
  if dayStart > 0:
    dayGood = 1  
else:
  nightStart = 0
  nightUsed = 0
  dayStart = 0 
  dayUsed = 0

while True:
 success = 0
 fail = 0
 while success == 0:
  try:
  # connect to inverter
   data = {
    'optType': 'ReadRealTimeData',
    'pwd': inverterPassword,
   }
   x = requests.post(inverterAddress, data=data)
   x = (x.text)
   cut = re.search("type",x)
   cut = cut.start()
   y = (x[cut+6:cut+8])
   if y != '15':
     display("Wrong type of inverter","red")
     time.sleep(30)
     break
   
   cut = re.search("Data",x)
   cut = cut.start()
   y = (x[cut+7:])
   array = re.split(",",y)
   y = array
   if (y[10] == 3) or (y[10] == 4):
     display("Inverter fault","red")
     time.sleep(30)
     continue

  except:
   display("Unable to contact inverter","red")

   if dchp == 1:
     inverterAddress = scan.ipScan(From, To, inverterPassword)
     if inverterAddress == None:
       display("Inverter not found","red")
       time.sleep(300)
       messageErased = 0
     else:
       inverterAddress = 'http://' + inverterAddress
       messageErased = 0
       success = 1
   else:
     fail = 1
     time.sleep(300)
   if pMessage != None:
     display(pMessage,"blue")
   else:
     messageErased = 0
   continue

  if cut > 0:
   success = 1
  else:
   fail = fail + 1
   if fail >= 6:
     display("Too many failures contacting inverter","red")
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

  total = (int(y[8])+int(y[9]))
  q = datetime.datetime.now()
  ntime = str(q.strftime("%X"))
  feedpower = float(y[32])

#  convert from twos somplement for negative numbers
  if feedpower > 32000:
    feedpower = 0
#  feedangle = (feedpower-2500)/2500*0.45
  batpower = float(y[16])
  batpower = 256*256 - batpower
  if batpower > 32000:
    batpower = -(256*256-batpower)
  if batpower < 0:
    batpower = 0
#  batangle = (batpower-2500)/2500*0.45
  
# clear pointers if relevant
  if int(total/100) != int(oldtotal/100):
   unpointer = Line(Point(pointstartx[int(oldtotal/100)], pointstarty[int(oldtotal/100)]), Point(pointendx[int(oldtotal/100)], pointendy[int(oldtotal/100)]))
   unpointer.setOutline("yellow")
   unpointer.setWidth(8)
   unpointer.draw(win)
  
  if ((int(feedpower/100) != int(oldfeedpower/100)) and (int(oldfeedpower/100) >= 0)) or (feedpower == 0):
   unfeedpointer = Line(Point(pointstartx[int(oldfeedpower/100)], pointstarty[int(oldfeedpower/100)]), Point(pointendx[int(oldfeedpower/100)], pointendy[int(oldfeedpower/100)]))
   unfeedpointer.setOutline("yellow")
   unfeedpointer.setWidth(8)
   unfeedpointer.draw(win)
   
  if ((int(batpower/100) != int(oldbatpower/100)) and (int(oldbatpower/100) >= 0)) or (batpower == 0):
   unbatpointer = Line(Point(pointstartx[int(oldbatpower/100)], pointstarty[int(oldbatpower/100)]), Point(pointendx[int(oldbatpower/100)], pointendy[int(oldbatpower/100)]))
   unbatpointer.setOutline("yellow")
   unbatpointer.setWidth(8)
   unbatpointer.draw(win)
 
  oldmode = mode

# create pointer for battery power
  if batpower > 0:
    if batpower > (scale*1000):
      batpower = scale*1000

    mode = 'bat'
  
    batpointer = Line(Point(pointstartx[int(batpower/100)], pointstarty[int(batpower/100)]), Point(pointendx[int(batpower/100)], pointendy[int(batpower/100)]))
    batpointer.setOutline("Blue")
    batpointer.setWidth(8)
    batpointer.draw(win)

# create pointer for feed to grid
  elif feedpower > 0:
    if feedpower > (scale*1000):
     feedpower = scale*1000
    mode = 'feed'

    feedpointer = Line(Point(pointstartx[int(feedpower/100)], pointstarty[int(feedpower/100)]), Point(pointendx[int(feedpower/100)], pointendy[int(feedpower/100)]))
    feedpointer.setOutline("Red")
    feedpointer.setWidth(8)
    feedpointer.draw(win)

  else:
    mode = 'none'

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

    
# create pointer for PV Power
  if total > (scale*1000):
    total = scale*1000
  pointer = Line(Point(pointstartx[int(total/100)], pointstarty[int(total/100)]), Point(pointendx[int(total/100)], pointendy[int(total/100)]))
  pointer.setOutline("Black")
  pointer.setWidth(8)
  pointer.draw(win)

# display state of charge
  rect = Rectangle(Point(450, 100), Point(540,300-(int(y[18])*2)))
  rect.setFill("White")
  rect.setOutline('Black')
  rect.draw(win)

  rect = Rectangle(Point(450,300-(int(y[18])*2)), Point(540,300))
  rect.setFill("Blue")
  rect.setOutline('Blue')
  rect.draw(win)


  if (float(y[32]) < 1) and (feed == 1):
    feed = 0 

  oldfeedpower = feedpower
  oldbatpower = batpower
  oldtotal = total

  consumeenergy = (int(y[37])*256*256+int(y[36]))/100

  feedinenergy = (int(y[35])*256*256+int(y[34]))/100

  yieldtotal = (int(y[12])*256*256+int(y[11]))/10

  nowTime= datetime.datetime.utcnow()
  localTime = datetime.datetime.now()
  if (int(nowTime.strftime("%H")) == 0) and (int(nowTime.strftime("%M")) == 0):
    nightStart = float(consumeenergy)
    nightGood = 1
    solDone = 0
    usedFailed = 1

  # erase preload message
  if (int(localTime.strftime("%H")) == 1) and (int(localTime.strftime("%M")) == 0):
    rect = Rectangle(Point(0,350), Point(800,400))
    rect.setFill("Light Gray")
    rect.setOutline('Light Gray')
    rect.draw(win)
    pMessage = None

    
  if (int(nowTime.strftime("%H")) == 7) and (int(nowTime.strftime("%M")) == 0):
    dayStart = float(consumeenergy)
    dayGood = 1
    startDayUsed = float(consumeenergy) + float(yieldtotal) - float(feedinenergy)
    usedFailed = 2

  if (int(nowTime.strftime("%H")) == 15) and (int(nowTime.strftime("%M")) == 0):
    endDayUsed = float(consumeenergy) + float(yieldtotal) - float(feedinenergy)
    todayUsed = endDayUsed - startDayUsed
    todayUsed = Week.means(todayUsed)
    if usedFailed == 2:
      usedFailed = 0

  if solcast.upper() == 'ON':
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
      display(pMessage,"blue")
      solDone = 1

      # set battery overnight preload
      if (preloadSet.upper() == "AUTO") and (type(preload) == int):
        preload = preload + offset
        if preload > 95:
          preload = 95
        elif preload < (offset + 10):
          preload = offset + 10
        pMessage = set.set(inverterAddress, inverterPassword, preload)  
        display(pMessage,"blue")
        solDone = 1
     
  if nightGood == 1:
    if (int(nowTime.strftime("%H")) >= startCheapRate and int(nowTime.strftime("%H")) < endCheapRate):
        nightUsed = int((consumeenergy - nightStart)*100)/100
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
        dayUsed =int((consumeenergy - dayStart)*100)/100
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

#Save localData
  if float(y[32]) != oldFeedIn: 
    localData = {"nightStart": nightStart, "nightUsed": nightUsed, "dayStart": dayStart, "dayUsed": dayUsed, "startDayUsed": startDayUsed, "endDayUsed": endDayUsed, "todayUsed": todayUsed}
    localDataJson = json.dumps(localData)

    f = open("power.json", "w")
    f.write(localDataJson)
    f.close()
    oldFeedIn = y[32]

  if float(y[32]) > 2500:
    charge = 1
  if (float(y[32]) < 0) and (charge == 1):
    charge = 0 
  time.sleep(30)
  t = t + 1 
