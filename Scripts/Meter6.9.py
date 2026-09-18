import Settings
import requests
import json
import datetime
import time
import math
import inspect
import os
import Solcast4
import Week2
import powerLog
import Octopus5
import threading

def watchdog():
    global watch
    global wait
    global hypCount
    while True:
        wait = 1
        waitTime = datetime.datetime.utcnow()
        period = 30 - int(waitTime.strftime("%S"))
        if watch == 1:
            watch = 2
        if period <= 0:
            period = period + 30
        time.sleep(period)
        hypCount = 0
        if watch == 2:
            errLog("Timeout")
            if Settings.run.upper() == "AUTO":
                os.system ('sudo reboot')
            else:
                print ("Timeout")

def disphy(hyphen):
    if hyphen == True:
        text = Text(Point(400,442)," : ")
        text._reconfig("font",("Arial",18,"bold"))
        text.setFill("Black")
        text.draw(win,0)
    else:
        rect = Rectangle(Point(397,430), Point(403,460))
        rect.setFill("Light Gray")
        rect.setOutline('Light Gray')
        rect.draw(win,0)

def dispclk(hrs,mins,ohrs,omins):
    if hrs != ohrs:
        rect = Rectangle(Point(350,430), Point(397,460))
        rect.setFill("Light Gray")
        rect.setOutline('Light Gray')
        text = Text(Point(380,445),hrs)
        text._reconfig("font",("Arial",18,"normal"))
        text.setFill("Black")
        rect.draw(win,0)
        text.draw(win,0)
        ohrs = hrs
    if mins != omins:
        rect = Rectangle(Point(397,430), Point(450,460))
        rect.setFill("Light Gray")
        rect.setOutline('Light Gray')
        text = Text(Point(420,445),mins)
        text._reconfig("font",("Arial",18,"normal"))
        text.setFill("Black")
        rect.draw(win,0)
        text.draw(win,0)
        omins = mins
    return ohrs,omins

def timeSleep(secs):
    dTime = 0
    while dTime < (secs*2):
        time.sleep(0.5)
        m = win.checkMouse()
        if m != None:
            if (m.x > 730) and (m.x < 800) and (m.y > 410) and (m.y < 480):
                win.master.state(newstate='iconic')
        dTime = dTime + 1
    return

# logging function
def errLog(exception):
    
    f = open("errlog.txt","a")
    f.write(str(datetime.datetime.now()) + "," + str(exception)+"\r")
    f.close()

def display(message,color):
    rect = Rectangle(Point(0,350), Point(800,400))
    rect.setFill("Light Gray")
    rect.setOutline('Light Gray')
    rect.draw(win,0)
    text = Text(Point(400,370),message)
    text._reconfig("font",("Arial",24,"bold"))
    text.setFill(color)
    text.draw(win,0)

# def disphy(hyphen):
#     if hyphen == True:
#         text = Text(Point(400,442)," : ")
#         text._reconfig("font",("Arial",18,"bold"))
#         text.setFill("Black")
#         text.draw(win,0)
#     else:
#         rect = Rectangle(Point(397,430), Point(403,460))
#         rect.setFill("Light Gray")
#         rect.setOutline('Light Gray')
#         rect.draw(win,0)

#Pause to allow GUI to initialise
if Settings.run.upper() == "AUTO":
    time.sleep(20)
    win_y = 0
else:
    win_y = 30

t1 = threading.Thread(target = watchdog)


# set current date and time
localTime = datetime.datetime.now()
if Settings.timeZone.upper() == "UTC":
  nowTime = datetime.datetime.utcnow()
else:
  nowTime = localTime

# set current date as yesterday if rebooting overnight
if int(localTime.strftime("%H")) < Settings.endCheapRate:
    yesterday = localTime - datetime.timedelta(days=1)
    currentDate = int(yesterday.strftime("%d"))
else:    
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
   
from graphics3 import *
win = GraphWin("Solar Power Meter",800,480)
win.master.geometry('%dx%d+%d+%d' % (800, 480, 0, 0))

rect = Rectangle(Point(0,0), Point(800,480))
rect.setFill('light gray')
rect.draw(win,0)

head = Circle(Point(200,480), 400) # set center and radius
head.setFill("yellow")
head.draw(win,0)

head = Circle(Point(200,480), 199) # set center and radius
head.setFill("light grey")
head.draw(win,0)

rect = Rectangle(Point(400, 0), Point(800,480))
rect.setFill("light grey")
rect.setOutline('light gray')
rect.draw(win,0)

# Get and draw three vertices of triangle
p1 = Point(0,80)
p1.draw(win,0)
p2 = Point(0,480)
p2.draw(win,0)
p3 = Point(200,480)
p3.draw(win,0)
vertices = [p1, p2, p3]

# Use Polygon object to draw the triangle
triangle = Polygon(vertices)
triangle.setFill('light gray')
triangle.setOutline('light gray')
triangle.setWidth(0)  # width of boundary line
triangle.draw(win,0)

# Get and draw three vertices of triangle
p1 = Point(400,80)
p1.draw(win,0)
p2 = Point(400,480)
p2.draw(win,0)
p3 = Point(200,480)
p3.draw(win,0)
vertices = [p1, p2, p3]

# Use Polygon object to draw the triangle
triangle = Polygon(vertices)
triangle.setFill('light gray')
triangle.setOutline('light gray')
triangle.setWidth(0)  # width of boundary line
triangle.draw(win,0) 


#Draw graduations
cal = 1
while cal < Settings.scale:
  angle = ((cal*1000)-(Settings.scale*500))/(Settings.scale*500)*0.45

  line = Line(Point(200+math.sin(angle)*400, 480-math.cos(angle)*400), Point(200+math.sin(angle)*360, 480-math.cos(angle)*360))
  line.setWidth(1)
  line.draw(win,0)
  text = Text(Point(200+math.sin(angle)*410,480-math.cos(angle)*410),str(cal))
  text.draw(win,0)
  cal = cal + 1

text = Text(Point(200,35),'PV power (kW)')
text.draw(win,0)

#Draw labels
text = Text(Point(535,35),'Battery State of Charge')
text.draw(win,0)

text = Text(Point(690,35),'Grid use today*')
text.draw(win,0)

text = Text(Point(680,290),'*while app running ')
text.draw(win,0)

text = Text(Point(400,290),'Export today')
text.draw(win,0)

#Draw battery
rect = Rectangle(Point(490, 100), Point(580,300))
rect.setFill("White")
rect.setWidth(3)
rect.setOutline('Black')
rect.draw(win,0)

rect = Rectangle(Point(520, 80), Point(550,100))
rect.setFill("Red")
rect.setOutline('Black')
rect.draw(win,0)

#Draw sun
sun = Circle(Point(680,100), 10) # set center and radius
sun.setFill("yellow")
sun.setOutline('Yellow')
sun.draw(win,0)

line = Line(Point(680,80), Point(680,120))
line.setWidth(3)
line.setOutline('Yellow')
line.draw(win,0)

line = Line(Point(666,86), Point(694,114))
line.setWidth(3)
line.setOutline('Yellow')
line.draw(win,0)

line = Line(Point(660,100), Point(700,100))
line.setWidth(3)
line.setOutline('Yellow')
line.draw(win,0)

line = Line(Point(666,114), Point(694,86))
line.setWidth(3)
line.setOutline('Yellow')
line.draw(win,0)

#Draw Moon
moon = Circle(Point(680,200), 10) # set center and radius
moon.setFill("White")
moon.setOutline('White')
moon.draw(win,0)

moon = Circle(Point(685,200), 8) # set center and radius
moon.setFill("Light Gray")
moon.setOutline('Light Gray')
moon.draw(win,0)

#get current directory
script_directory = os.path.dirname(os.path.abspath( 
inspect.getfile(inspect.currentframe()))) 

if Settings.run.upper() == "AUTO":
    myImage = Image(Point(765,445), 0, 0, script_directory +  "/Exit.gif")
    myImage.draw(win,0)

location = 3
pylon = Image(Point(420, 175), 22, location, script_directory + "/Pylon_80_anim.gif")
pylon.draw(win, location)

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
tomUsed = 0
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
logDone = 1
export = 0
offset = Settings.offset
fStartHrs = 0
fStartMins = 0
fEndHrs = 0
fEndMins = 0
freeSet = 0
freeDone = 0
ssSet = 0
solcast = Settings.solcast.upper()
preloadSet = Settings.preloadSet.upper()
dischargeDelay = Settings.dischargeDelay.upper()
if Settings.octopus.upper() == "YES":
    octopus = "ON"
else:
    octopus = "OFF"
setPreload = 95
feedinenergy = 0
oldFeedEnergy = 0
firstPass = 0
efficiency = 80
if Settings.octopus.upper() == "YES":
    octopus = "ON"
else:
    octopus = "OFF"
octDone = 0
sHrs = 25 #Time that can never occur
sMins = 0
hrs = Settings.noDelay
mins = 0
boostMode = 0
boost = 0
boostStartHrs = 0
boostStartMins = 0
boostEndHrs = 0
boostEndMins = 0
dayGrid = 0
nightGrid = 0
oldDayGrid = 0
oldNightGrid = 0
exportGrid = 0
oldExportGrid = 0
logDone = 0
# software watchdog
watch = 0
# 0 = disabled
# 1 = enabled - active
# 2 = enabled - timing out
wait = 0
hyphen = 0
hypCount = 0
ohrs = ""
omins = ""

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
    try:
        localData = json.loads(localDataJson)
        recordDate = localData["Date"]
        if currentDate == recordDate:
            dateError = 0
            setDate = recordDate
            nightStart = localData["nightStart"]
            nightUsed = localData["nightUsed"]
            lastNightUsed = round(nightGrid,2)
            dayStart = localData["dayStart"]
            dayUsed = localData["dayUsed"]
            startDayUsed = localData["startDayUsed"]
            endDayUsed = localData["endDayUsed"]
            todayUsed = localData["todayUsed"]
            tomUsed = localData["tomUsed"]
            efficiency = localData["efficiency"]
            solarYield = localData["solarYield"]
            batteryUse = localData["batteryUse"]
            try:
                dayGrid = localData["dayGrid"]
                nightGrid = localData["nightGrid"]
                exportGrid = localData["exportGrid"]
                lastNightUsed = nightGrid
            except:
                dayGrid = localData["dayUsed"]
                nightGrid = localData["nightUsed"]
                exportGrid = localData["export"]
                lastNightUsed = nightUsed
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
    except:
        f.close()
        dateError = 1
        pMessage = "Corrupt backup file"
        errLog (pMessage)
        os.remove("power.json")
        if Settings.run.upper() != "AUTO":
            print (pMessage)
      
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
  
t1.start()

try: 
    while True:
     while wait == 0:
         timeSleep(0.5)
         watch = 1
         if Settings.run.upper() == "AUTO":
             hyphen = not hyphen
             disphy(hyphen)
             hypCount = hypCount + 1
             if hypCount >= 300:
                 errLog("Timing loop has stopped")
                 if Settings.run.upper() == "AUTO":
                     os.system ('sudo reboot')
                 else:
                     print("Timing loop has stopped")
         m = win.checkMouse()
         if m != None:
             if (m.x > 730) and (m.x < 800) and (m.y > 410) and (m.y < 480):
                win.master.state(newstate='iconic')
     wait = 0
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
       timeSleep(300)
       messageErased = 0
       continue
      if str(y["success"]) == "True":
       success = 1
      else:
       fail = fail + 1
       if fail >= 6:
         display("Too many failures contacting cloud","red")
         timeSleep(300) 

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
        rect.draw(win,0)
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
      if feedpower < 0:
        gridPower = -feedpower
      else:
        gridPower = 0
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
       unpointer.draw(win,0)
      
      if ((int(chargepower/100) != int(oldcharge/100)) and (int(oldcharge/100) >= 0)) or (chargepower == 0) or (feedpower > chargepower):
       pcoldcharge = oldcharge/100
       unchargepointer = Line(Point(pointstartx[int(pcoldcharge)], pointstarty[int(pcoldcharge)]), Point(pointendx[int(pcoldcharge)], pointendy[int(pcoldcharge)]))
       unchargepointer.setOutline("yellow")
       unchargepointer.setWidth(8)
       unchargepointer.draw(win,0)
       
      if ((int(feedpower/100) != int(oldfeedpower/100)) and (int(oldfeedpower/100) >= 0)) or (feedpower == 0):
       pcoldfeedpower = oldfeedpower/100
       unfeedpointer = Line(Point(pointstartx[int(pcoldfeedpower)], pointstarty[int(pcoldfeedpower)]), Point(pointendx[int(pcoldfeedpower)], pointendy[int(pcoldfeedpower)]))
       unfeedpointer.setOutline("yellow")
       unfeedpointer.setWidth(8)
       unfeedpointer.draw(win,0)
       
      if ((int(batpower/100) != int(oldbatpower/100)) and (int(oldbatpower/100) >= 0)) or (batpower == 0):
       pcoldbatpower = oldbatpower/100
       unbatpointer = Line(Point(pointstartx[int(pcoldbatpower)], pointstarty[int(pcoldbatpower)]), Point(pointendx[int(pcoldbatpower)], pointendy[int(pcoldbatpower)]))
       unbatpointer.setOutline("yellow")
       unbatpointer.setWidth(8)
       unbatpointer.draw(win,0)


    #write pointer for charge power
      if mode == 'charge':
        chargepointer = Line(Point(pointstartx[int(pcchargepower)], pointstarty[int(pcchargepower)]), Point(pointendx[int(pcchargepower)], pointendy[int(pcchargepower)]))
        chargepointer.setOutline("Green")
        chargepointer.setWidth(8)
        chargepointer.draw(win,0)

    #write pointer for battery power
      if mode == 'bat':
        batpointer = Line(Point(pointstartx[int(pcbatpower)], pointstarty[int(pcbatpower)]), Point(pointendx[int(pcbatpower)], pointendy[int(pcbatpower)]))
        batpointer.setOutline("Blue")
        batpointer.setWidth(8)
        batpointer.draw(win,0)

    #write pointer for feed to grid
      if mode == 'feed':
        feedpointer = Line(Point(pointstartx[int(pcfeedpower)], pointstarty[int(pcfeedpower)]), Point(pointendx[int(pcfeedpower)], pointendy[int(pcfeedpower)]))
        feedpointer.setOutline("Red")
        feedpointer.setWidth(8)
        feedpointer.draw(win,0)

      if mode != oldmode:
        #remove text
        rect = Rectangle(Point(0,305), Point(400,350))
        rect.setFill("Light Gray")
        rect.setOutline('Light Gray')
        rect.draw(win,0)

      if mode == 'bat':
        text = Text(Point(200,320),'Battery power')
        text.setOutline("Blue")
        text.draw(win,0)
      elif mode == 'feed':
        text = Text(Point(200,320),'Power to grid')
        text.setOutline("Red")
        text.draw(win,0)
      elif mode == 'charge':
        text = Text(Point(200,320),'Charging')
        text.setOutline("Green")
        text.draw(win,0)

    # create pointer for PV Power
      if total > (Settings.scale*1000):
        total = Settings.scale*1000
      pctotal = total/100

    # draw pointer for PV power
      pointer = Line(Point(pointstartx[int(pctotal)], pointstarty[int(pctotal)]), Point(pointendx[int(pctotal)], pointendy[int(pctotal)]))
      pointer.setOutline("Black")
      pointer.setWidth(8)
      pointer.draw(win,0)

    # display state of charge
      rect = Rectangle(Point(490, 100), Point(580,300-(y["soc"]*2)))
      rect.setFill("White")
      rect.setOutline('Black')
      rect.draw(win,0)

      rect = Rectangle(Point(490,300-(y["soc"]*2)), Point(580,300))
      rect.setFill("Blue")
      rect.setOutline('Blue')
      rect.draw(win,0)

    # accumulate solar radiation total
      solarYield = solarYield + (total/120000)
    # accumulate battery outpout total
      batteryUse = batteryUse + (batpower/120000)
    # accumulate export power
      export = export + feedinenergy - oldFeedEnergy
      feedInGrid = (y["feedinpower"]/120000)
      if feedInGrid < 0:
          feedInGrid = 0
      exportGrid = exportGrid + feedInGrid
      if export > exportGrid:
        exportGrid = export
      
    # accumulate grid power
      if dayGood == 1:
          dayGrid = dayGrid + (gridPower/120000)
      elif nightGood == 1:
          nightGrid = nightGrid + (gridPower/120000)

      if (float(y['feedinpower']) < 1) and (feed == 1):
        feed = 0 

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

      # display clock
      if Settings.run.upper() == "AUTO":
        ohrs,omins = dispclk(nowTime.strftime("%H"),nowTime.strftime("%M"),ohrs,omins)
            
      if nowTimeMins == Settings.startCheapRate:
        nightStart = float(y["consumeenergy"])
        nightGrid = 0
        nightGood = 1
        noFile = 0
        solDone = 0
        usedFailed = 1

      # Check National Grid website for an Octopus Saving Session
      if (octopus == "ON") and (octDone == 0):
          if (int(localTime.strftime("%H")) >= 9) and (int(localTime.strftime("%H")) < 21) and (int(localTime.strftime("%M")) == 5) and (int(localTime.strftime("%S")) < 30):
              ssDelay = Octopus5.check()
              ssSet = ssDelay[1]
              octDone = 1
              if ssDelay[0] != "":
                  octDone = 2
                  pMessage = ssDelay[0]
                  display(pMessage,"blue")
                  delaySet = 2
                  sHrs = ssDelay[2]
                  sMins = ssDelay[3]
                  fEndHrs = ssDelay[4]
                  fEndMins = ssDelay[5]
                  setData = {"solcast" :solcast, "preloadSet":preloadSet, "dischargeDelay":dischargeDelay, "setPreload":setPreload,"octopus":octopus,"ssSet":ssSet,
                  "sHrs":sHrs,"sMins":sMins,"fStartHrs":fStartHrs, "fStartMins":fStartMins, "fEndHrs":fEndHrs, "fEndMins":fEndMins, "freeSet":freeSet,
                  "freeDone":freeDone, "boostMode": boostMode, "boostStartHrs": boostStartHrs, "boostStartMins": boostStartMins, "boostEndHrs": boostEndHrs, "boostEndMins": boostEndMins, "boost": boost}
                  setDataJson = json.dumps(setData)
                  f = open("set_bak.json", "w")
                  f.write(setDataJson)
                  f.close()

      # erase preload message
      if (int(localTime.strftime("%H")) == 1) and (int(localTime.strftime("%M")) == 0):
        rect = Rectangle(Point(0,350), Point(800,400))
        rect.setFill("Light Gray")
        rect.setOutline('Light Gray')
        rect.draw(win,0)
        pMessage = None
     
      if nowTimeMins == Settings.endCheapRate:
        currentDate = int(localTime.strftime("%d"))
        setDate = currentDate #only update date at start of daytime period
        dateError = 0
        dayStart = float(y["consumeenergy"])
        dayGood = 1
        startDayUsed = float(y["consumeenergy"]) + float(y["yieldtotal"]) - float(y["feedinenergy"])
        usedFailed = 2
        lastNightUsed = nightGrid
        exportGrid = export
        dayGrid = 0

      if (int(localTime.strftime("%H")) == 15) and (int(localTime.strftime("%M")) == 0):
        endDayUsed = float(y["consumeenergy"]) + float(y["yieldtotal"]) - float(y["feedinenergy"])
        todayUsed = endDayUsed - startDayUsed
        logDone = 0
        noFile = 0
        if dateError == 0:
          todayUsed = Week2.means(todayUsed)
        if usedFailed == 2:
          usedFailed = 0

      if Settings.solcast.upper() == 'ON':
        if (int(localTime.strftime("%H")) >= 21) and (solDone != 1):
          if True:
            if usedFailed == 0: 
              preload = Solcast4.getForecast(todayUsed)
            else:
              preload = Solcast4.getForecast(7,85)
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

      #Draw Pylon
      script_directory = os.path.dirname(os.path.abspath( 
        inspect.getfile(inspect.currentframe()))) 

      if (round(exportGrid,2) != round(oldExportGrid,2)) or (oldfeedpower == 0):
          if feedpower > 0:
              location = 24
          elif feedpower < 0:
              location = 25
          else:
              location = 23
                          
          pylon.animate(win,location)

          if exportGrid > 0:
            rect = Rectangle(Point(340,240 ), Point(460,260))
            rect.setFill("Light Gray")
            rect.setOutline('Light Gray')
            rect.draw(win,0)
            time.sleep(0.04)
            text = Text(Point(400,250), str(round(exportGrid,2)) + " kWh")
            text._reconfig("font",("Arial",18,"normal"))
            text.draw(win,0)


      if noFile == 0:
        if nightGood == 1:
          if (nowTimeMins >= Settings.startCheapRate) and (nowTimeMins < Settings.endCheapRate):
            nightUsed = int((y["consumeenergy"] - nightStart)*100)/100
          else:
            nightGood = 0     
          if oldNightGrid != nightGrid:
            rect = Rectangle(Point(620,240 ), Point(800,260))
            rect.setFill("Light Gray")
            rect.setOutline('Light Gray')
            rect.draw(win,0)
            text = Text(Point(680,250), str(round(nightGrid,2)) + " kWh")
            text._reconfig("font",("Arial",18,"normal"))
            text.draw(win,0)
            oldNightUsed = nightUsed
            oldfeedpower = 0
          
        if dayGood == 1:
          if not((nowTimeMins >= Settings.startCheapRate) and (nowTimeMins < Settings.endCheapRate)):
            dayUsed = int((y["consumeenergy"] - dayStart)*100)/100
          else:
            dayGood = 0                                                
          if oldDayGrid != dayGrid:
            rect = Rectangle(Point(620,140 ), Point(800,160))
            rect.setFill("Light Gray")
            rect.setOutline('Light Gray')
            rect.draw(win,0)
            text = Text(Point(680,150), str(round(dayGrid,2)) + " kWh")
            text._reconfig("font",("Arial",18,"normal"))
            text.draw(win,0)
            oldDayUsed = dayUsed
            oldDayGrid = dayGrid

      oldfeedpower = feedpower
      oldbatpower = batpower
      oldtotal = total
      oldcharge = chargepower
      oldDayUsed = dayUsed
      oldExportGrid = exportGrid


    #Save data
      if ((float(y['feedinpower']) != oldFeedIn) or (gridPower != 0)) and (dateError == 0): 
        localData = {"Date": setDate, "nightStart": nightStart, "nightUsed": nightUsed, "dayStart": dayStart, "dayUsed": dayUsed, "startDayUsed": startDayUsed, "endDayUsed":
        endDayUsed, "todayUsed": todayUsed, "tomUsed": tomUsed, "efficiency": efficiency, "solarYield": solarYield, "batteryUse": batteryUse, "dayGrid": dayGrid, "nightGrid": nightGrid,
        "export": export, "exportGrid": exportGrid}
        localDataJson = json.dumps(localData)
        f = open("power.json", "w")
        f.write(localDataJson)
        f.close()
        oldFeedIn = float(y['feedinpower'])

      oldtotal = total

      if feedpower < 0:
        feedpower = 0

      # Send data to log
      if (Settings.log.upper() == "YES") and (logDone == 0) and (nowTimeMins == Settings.startCheapRate):
          logDone = powerLog.logPower(round(dayGrid,2),lastNightUsed,solarYield,round(batteryUse,2),exportGrid)
          if logDone == 1:
              solarYield = 0
              batteryUse = 0
              export = 0
              exportGrid = 0
              oldFeedIn = y['feedinpower']

except Exception as e:
    errLog(e)
    if Settings.run.upper() == "AUTO":
        watch = 2
    else:
        raise
