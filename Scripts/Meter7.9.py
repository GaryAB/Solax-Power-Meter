import requests
import inspect
import json
import datetime
import time
import math
import os
import Solcast4
import Week2
import re
import scan
import set3
import powerLog
import Octopus5
import Settings
import threading
import Info4
import FreeFind2
import Boost2

v = 0

# logging function
def errLog(exception):

    f = open("errlog.txt", "a")
    f.write(str(datetime.datetime.now()) + "," + str(exception) + "\r")
    f.close()

def display(message, colour):
    rect = Rectangle(Point(64, 350), Point(800, 400))
    rect.setFill("Light Gray")
    rect.setOutline("Light Gray")
    rect.draw(win, 0)
    text = Text(Point(400, 370), message)
    text._reconfig("font", ("Arial", 24, "bold"))
    text.setFill(colour)
    text.draw(win, 0)

def disphy(hyphen):
    if hyphen == True:
        text = Text(Point(400, 442), " : ")
        text._reconfig("font", ("Arial", 18, "bold"))
        text.setFill("Black")
        text.draw(win, 0)
    else:
        text = Text(Point(400, 442), " : ")
        text._reconfig("font", ("Arial", 18, "bold"))
        text.setFill("Light Gray")
        text.draw(win, 0)

def dispclk(hrs, mins, ohrs, omins):
    if hrs != ohrs:
        rect = Rectangle(Point(350, 430), Point(397, 460))
        rect.setFill("Light Gray")
        rect.setOutline("Light Gray")
        text = Text(Point(380, 445), hrs)
        text._reconfig("font", ("Arial", 18, "normal"))
        text.setFill("Black")
        rect.draw(win, 0)
        text.draw(win, 0)
        ohrs = hrs
    if mins != omins:
        rect = Rectangle(Point(397, 430), Point(450, 460))
        rect.setFill("Light Gray")
        rect.setOutline("Light Gray")
        text = Text(Point(420, 445), mins)
        text._reconfig("font", ("Arial", 18, "normal"))
        text.setFill("Black")
        rect.draw(win, 0)
        text.draw(win, 0)
        omins = mins
    return ohrs, omins


# Timing thread starts here


def threadTest():
    a = 0
    while True:
        a = a + 1
        global success
        success = 0
        searchCounter = 0
        global fail
        fail = 0
        global wait
        global messageErased
        global inverterAddress
        global y
        global invReturn
        global pMessage
        global message
        global watch
        global period
        global hypCount
        xMessage = pMessage
        error = 0
        tryCount = 0
        currentDate = int(localTime.strftime("%d"))
        while True:
            time.sleep(1)
            hypCount = 0
            try:
                while True:
                    # connect to inverter
                    data = {
                        "optType": "ReadRealTimeData",
                        "pwd": Settings.inverterPassword,
                    }
                    invReturn = requests.post(inverterAddress, data=data)
                    invReturn = invReturn.text

                    wait = 1
                    waitTime = datetime.datetime.utcnow()
                    period = 15 - int(waitTime.strftime("%S"))
                    watch = watch + 1
                    while period <= 0:
                        period = period + 15
                    time.sleep(period)
                    hypCount = 0
                    if watch >= 4:
                        errLog("Timeout")
                        if Settings.run.upper() == "AUTO":
                            os.system("sudo reboot")
                        else:
                            print("Timeout")
                            quit()
            except Exception as e:
                if tryCount < 5:
                    hypCount = 0
                    time.sleep(20)
                    tryCount = tryCount + 1
                    continue
                tryCount = 0
                errLog(e)
                success = 0
                searchCounter = 0
                while success == 0:
                    if Settings.inverterAddress.upper() == "DHCP":
                        inverterAddress = scan.ipScan(
                            Settings.From, Settings.To, Settings.inverterPassword
                        )
                        if inverterAddress == None:
                            pMessage = "Inverter not found"
                            time.sleep(20)
                            messageErased = 0
                            watch = 2
                            success = 0
                            hypCount = 0
                        else:
                            inverterAddress = "http://" + inverterAddress
                            pMessage = xMessage
                            if pMessage == None:
                                messageErased = 1
                            else:
                                messageErased = 0
                            success = 1
                            tryCount = 0
                    else:
                        inverterAddress = "http://" + Settings.inverterAddress
                        pMessage = xMessage
                        messageErased = 0
                        success = 1
                    if pMessage == None:
                        messageErased = 0
                    if success == 0:
                        hypCount = 0
                        searchCounter = searchCounter + 1
                        time.sleep(60)
                        if pMessage == None:
                            errLog(str(searchCounter) + " attempts to find inverter")
                        else:
                            errLog(pMessage)
                            if Settings.run.upper() == "AUTO":
                                os.system("sudo reboot")
                            else:
                                print(pMessage)


# End of timing thread

# Pause to allow GUI to initialise
if Settings.run.upper() == "AUTO":
    time.sleep(20)
    win_y = 0
else:
    win_y = 30

# Full program starts here

t1 = threading.Thread(target=threadTest)

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

# Create look-up tables
pangle = -0.45
pointstartx = [200 + math.sin(pangle) * 200]
pointstarty = [480 - math.cos(pangle) * 200]
pointendx = [200 + math.sin(pangle) * 360]
pointendy = [480 - math.cos(pangle) * 360]
a = 0
while a <= Settings.scale * 10:
    pangle = (int(a * 100) - (Settings.scale * 500)) / (Settings.scale * 500) * 0.45
    pointstartx.append(200 + math.sin(pangle) * 200)
    pointstarty.append(480 - math.cos(pangle) * 200)
    pointendx.append(200 + math.sin(pangle) * 360)
    pointendy.append(480 - math.cos(pangle) * 360)
    a = a + 1

from graphics3 import *

win = GraphWin("Solar Power Meter", 800, 480)
win.master.geometry("%dx%d+%d+%d" % (800, 480, 0, win_y))

rect = Rectangle(Point(0, 0), Point(800, 480))
rect.setFill("light gray")
rect.draw(win, 0)

head = Circle(Point(200, 480), 400)  # set center and radius
head.setFill("yellow")
head.draw(win, 0)

head = Circle(Point(200, 480), 199)  # set center and radius
head.setFill("light grey")
head.draw(win, 0)

rect = Rectangle(Point(400, 0), Point(800, 480))
rect.setFill("light grey")
rect.setOutline("light gray")
rect.draw(win, 0)

# Get and draw three vertices of triangle
p1 = Point(0, 80)
p1.draw(win, 0)
p2 = Point(0, 480)
p2.draw(win, 0)
p3 = Point(200, 480)
p3.draw(win, 0)
vertices = [p1, p2, p3]

# Use Polygon object to draw the triangle
triangle = Polygon(vertices)
triangle.setFill("light gray")
triangle.setOutline("light gray")
triangle.setWidth(0)  # width of boundary line
triangle.draw(win, 0)

# Get and draw three vertices of triangle
p1 = Point(400, 80)
p1.draw(win, 0)
p2 = Point(400, 480)
p2.draw(win, 0)
p3 = Point(200, 480)
p3.draw(win, 0)
vertices = [p1, p2, p3]

# Use Polygon object to draw the triangle
triangle = Polygon(vertices)
triangle.setFill("light gray")
triangle.setOutline("light gray")
triangle.setWidth(0)  # width of boundary line
triangle.draw(win, 0)


# Draw graduations
cal = 1
while cal < Settings.scale:
    angle = ((cal * 1000) - (Settings.scale * 500)) / (Settings.scale * 500) * 0.45

    line = Line(
        Point(200 + math.sin(angle) * 400, 480 - math.cos(angle) * 400),
        Point(200 + math.sin(angle) * 360, 480 - math.cos(angle) * 360),
    )
    line.setWidth(1)
    line.draw(win, 0)
    text = Text(
        Point(200 + math.sin(angle) * 410, 480 - math.cos(angle) * 410), str(cal)
    )
    text.draw(win, 0)
    cal = cal + 1


text = Text(Point(200, 35), "PV power (kW)")
text.draw(win, 0)

# Draw labels
text = Text(Point(535, 35), "Battery State of Charge")
text.draw(win, 0)

text = Text(Point(690, 35), "Grid use today*")
text.draw(win, 0)

text = Text(Point(680, 290), "*while app running ")
text.draw(win, 0)

text = Text(Point(400, 290), "Export today")
text.draw(win, 0)

# Draw battery
rect = Rectangle(Point(490, 100), Point(580, 300))
rect.setFill("White")
rect.setWidth(3)
rect.setOutline("Black")
rect.draw(win, 0)

rect = Rectangle(Point(520, 80), Point(550, 100))
rect.setFill("Red")
rect.setOutline("Black")
rect.draw(win, 0)

# Draw sun
sun = Circle(Point(680, 100), 10)  # set center and radius
sun.setFill("yellow")
sun.setOutline("Yellow")
sun.draw(win, 0)

line = Line(Point(680, 80), Point(680, 120))
line.setWidth(3)
line.setOutline("Yellow")
line.draw(win, 0)

line = Line(Point(666, 86), Point(694, 114))
line.setWidth(3)
line.setOutline("Yellow")
line.draw(win, 0)

line = Line(Point(660, 100), Point(700, 100))
line.setWidth(3)
line.setOutline("Yellow")
line.draw(win, 0)

line = Line(Point(666, 114), Point(694, 86))
line.setWidth(3)
line.setOutline("Yellow")
line.draw(win, 0)

# Draw Moon
moon = Circle(Point(680, 200), 10)  # set center and radius
moon.setFill("White")
moon.setOutline("White")
moon.draw(win, 0)

moon = Circle(Point(685, 200), 8)  # set center and radius
moon.setFill("Light Gray")
moon.setOutline("Light Gray")
moon.draw(win, 0)

# Draw Cogwheel, Exit and Timer symbols

script_directory = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)

location = 0
myImage = Image(Point(35, 35), 0, location, script_directory + "/Cog.gif")
myImage.draw(win, location)
location = 1
if Settings.run.upper() == "AUTO":
    myImage = Image(Point(765, 445), 0, location, script_directory + "/Exit.gif")
    myImage.draw(win, location)
location = 2
if Settings.run.upper() == "AUTO":
    myImage = Image(Point(35, 445), 0, location, script_directory + "/Timer.gif")
else:
    myImage = Image(Point(35, 380), 0, location, script_directory + "/Timer.gif")
myImage.draw(win, location)
location = 3
myImage = Image(Point(420, 175), 20, location, script_directory + "/Pylon_80_anim.gif")
myImage.draw(win, location)

# Initilise variables
t = 0
charge = 0
feed = 0
y = {}
invReturn = " "
mode = "none"
feedpower = 0
oldfeedpower = 0
oldbatpower = 0
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
dhcp = 0
pMessage = None
noFile = 0
chgReg = 31  # Register to set charge limit
dchReg = 39  # Register to set discharge start time
modeReg = 28  # Register to change work mode
forceReg = 36  # Register to force charge or discharge
selfMode = 0  # Setting for Self Use mode
manualMode = 3  # Setting for Manual mode
forceCharge = 1  # Setting for manual mode force charge
delayTime = Settings.noDelay
delaySet = 0
solarYield = 0
batteryUse = 0
logDone = 0
export = 0
feedinenergy = 0
oldFeedEnergy = 0
firstPass = 0
sHrs = 25  # Time that can never occur
sMins = 0
hrs = Settings.noDelay
mins = 0
octDone = 0
message = ""
error = ""
inverterAddress = Settings.inverterAddress
offset = Settings.offset
fStartHrs = 0
fStartMins = 0
fEndHrs = 0
fEndMins = 0
freeSet = 0
freeDone = 0
ssSet = 0
ssExport = Settings.ssExport.upper()
ssActive = 0
solcast = Settings.solcast.upper()
preloadSet = Settings.preloadSet.upper()
dischargeDelay = Settings.dischargeDelay.upper()
if Settings.octopus.upper() == "YES":
    octopus = "ON"
else:
    octopus = "OFF"
setPreload = 95
tomUsed = 7
hyphen = True
hypCount = 0
ohrs = ""
omins = ""
lsuccess = 0
efficiency = 80
# software watchdog
watch = 0
# 0 = disabled
# 1 = enabled - active
# 2 = enabled - timing out
boostMode = 0
boost = 0
boostStartHrs = 0
boostStartMins = 0
boostEndHrs = 0
boostEndMins = 0
iMessage = ""
dayUsed = 0
dayGrid = 0
oldDayGrid = 0
oldNightGrid = 0
nightUsed = 0
nightGrid = 0
exportGrid = 0
oldExportGrid = 0
gridPower = 0
oldGridPower = 1
limit = 10
newLimit = 10
perm = "OFF"
default = 0
hypWait = 0
carCharge = 2
oldConsume = 0
carStart = 15127 #23:59 so end of day.

dchReg = 39  # Register to set discharge start time
chgReg = 31  # Register to set charge limit
modeReg = 28  # Register to set working mode
manReg = 36  # Register to adjust manual mode
selfMode = 0  # Setting for Self Use mode
manualMode = 3  # Setting for Manual mode

# setcheaprate times to minutes from 12 noon
if Settings.startCheapRate < 12:
    Settings.startCheapRate = (Settings.startCheapRate + 12) * 60 + Settings.crMins
else:
    Settings.startCheapRate = (Settings.startCheapRate - 12) * 60 + Settings.crMins
if Settings.endCheapRate < 12:
    Settings.endCheapRate = (Settings.endCheapRate + 12) * 60 + Settings.prMins
else:
    Settings.endCheapRate = (Settings.endCheapRate - 12) * 60 + Settings.prMins
wait = 0

if inverterAddress.upper() == "DHCP":
    dhcp = 1
    while lsuccess == 0:
        inverterAddress = scan.ipScan(
            Settings.From, Settings.To, Settings.inverterPassword
        )
        if inverterAddress == None:
            text = Text(Point(400, 370), "Inverter not found")
            text._reconfig("font", ("Arial", 24, "bold"))
            text.setFill("Red")
            text.draw(win, 0)
            time.sleep(30)
            messageErased = 0
            lsuccess = 0
        else:
            inverterAddress = "http://" + inverterAddress
            lsuccess = 1
            messageErased = 0
else:
    inverterAddress = "http://" + inverterAddress

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
            lastNightUsed = nightUsed
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
                lastNightUsed = round(nightGrid, 2)
            except:
                dayGrid = localData["dayUsed"]
                nightGrid = localData["nightUsed"]
                exportGrid = localData["export"]
                lastNightUsed = nightUsed
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
    except:
        f.close()
        dateError = 1
        pMessage = "Corrupt backup file"
        errLog(pMessage)
        os.remove("power.json")
        if Settings.run.upper() != "AUTO":
            print(pMessage)

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

if os.path.exists("set_bak.json"):
    try:
        f = open("set_bak.json", "r")
        setDataJson = f.read()
        setData = json.loads(setDataJson)
        solcast = setData["solcast"]
        preloadSet = setData["preloadSet"]
        setPreload = setData["setPreload"]
        dischargeDelay = setData["dischargeDelay"]
        octopus = setData["octopus"]
        ssSet = setData["ssSet"]
        ssExport = setData["ssExport"]
        sHrs = setData["sHrs"]
        sMins = setData["sMins"]
        fStartHrs = setData["fStartHrs"]
        fStartMins = setData["fStartMins"]
        fEndHrs = setData["fEndHrs"]
        fEndMins = setData["fEndMins"]
        freeSet = setData["freeSet"]
        freeDone = setData["freeDone"]
        boostMode = setData["boostMode"]
        boostStartHrs = setData["boostStartHrs"]
        boostStartMins = setData["boostStartMins"]
        boostEndHrs = setData["boostEndHrs"]
        boostEndMins = setData["boostEndMins"]
        boost = setData["boost"]
        limit = setData["limit"]
        perm = setData["perm"]
    except:
        f.close()
        os.remove("set_bak.json")
        errLog("Settings backup corrupt, using default settings")
        default = 1
        pMessage = "Using default settings"
        display(pMessage, "Red")


# Checkfor battery delay
data = "optType=ReadSetData&pwd=" + Settings.inverterPassword
x = requests.post(inverterAddress, data=data)
x = x.text
y = x[1:]
array = re.split(",", y)
delayTime = array[dchReg - 1]
mins = int(int(delayTime) / 256)
hrs = int(delayTime) - (mins * 256)
if delayTime != Settings.noDelay:
    delaySet = 1

time.sleep(5)

timer = 0
num = 4
oldTime = int(localTime.strftime("%f"))
drawn = 0
m = None

myImage = Image(Point(420, 175), 20, 4, script_directory + "/Pylon_80_anim.gif")

try:
    # first check current settings and save them
    # Do not sasve if CharegStart is set to midnight as a function has alreasy saved them.
    data = 'optType=ReadSetData&pwd='+ Settings.inverterPassword
    x = requests.post(inverterAddress, data=data)
    x = (x.text)
    y = x[1:]
    array = re.split(",",y)
    invMode = array[27]
    chargeStart = array[36]
    chargeEnd = array[37]
    dischargeStart = array[38]
    dischargeEnd = array[39]

    Info4.saveTimes(chargeStart,chargeEnd,dischargeStart,dischargeEnd)

    # Test for Mouse clicks whilst waiting for thread to update data from inverter
    while True:
        watch = 1
        while (wait == 0) or (hypWait != 0):
            watch = 1
            # Create and display pylon animation. The image file is uploaded to a buffer from which it is displayed.
            # Requires specially modified version of graphics.py.
            if feedpower > 0:
                first = 5
                frames = 10
            elif gridPower > 0:
                first = 15
                frames = 10
            else:
                first = 5
                frames = 0
            last = first + frames

            if frames > 0:
                myImage.animate(win, num)
                time.sleep(0.1)
                myImage.unanimate()
                num = num + 1
                if num >= last:
                    num = first
                    hypWait = 9
            else:
                time.sleep(0.1)
                hypWait = hypWait + 1
                if hypWait >= 10:
                    hypWait = 0

            if Settings.run.upper() == "AUTO":
                if hypWait == 9:
                    hyphen = not hyphen
                    disphy(hyphen)
            hypCount = hypCount + 1
            if hypCount >= 3000:
                errLog("Timing loop has stopped")
                if Settings.run.upper() == "AUTO":
                    os.system("sudo reboot")
                else:
                    print("Timing loop has stopped")
                hypCount = 0
            hypWait = 0
            m = win.checkMouse()
            if m != None:
                if (m.x > 0) and (m.x < 70) and (m.y > 0) and (m.y < 70):
                    if dischargeDelay == "AUTO":
                        dischargeDelay = "ON"
                    else:
                        dischargeDelay = "OFF"
                    if preloadSet == "AUTO":
                        preloadSet = "ON"
                    else:
                        preloadSet = "OFF"
                    if freeSet != 0:
                        freeTag = "ON"
                    else:
                        freeTag = "OFF"
                    watch = 0
                    (
                        solcast,
                        preloadSet,
                        dischargeDelay,
                        setPreload,
                        octopus,
                        ssExport,
                        freeTag,
                        fStartHrs,
                        fStartMins,
                        fEndHrs,
                        fEndMins,
                        offset,
                    ) = Info4.info(
                        inverterAddress,
                        solcast,
                        preloadSet,
                        dischargeDelay,
                        setPreload,
                        octopus,
                        ssExport,
                        freeTag,
                        fStartHrs,
                        fStartMins,
                        fEndHrs,
                        fEndMins,
                        offset,
                        win,
                    )
                    watch = 1
                    if default == 1:
                        default = 0
                        pMessage = ""
                        display(pMessage, "blue")
                    if type(setPreload) != str:
                        preload = int(setPreload) - int(offset)
                        if type(pMessage) == str:
                            if pMessage[0:17] == "Preload is set to":
                                pMessage = "Preload is set to " + str(setPreload) + "%"
                                display(pMessage, "blue")
                    if freeTag == "ON":
                        freeSet = 1
                    else:
                        freeSet = 0
                    if dischargeDelay == "ON":
                        dischargeDelay = "AUTO"
                    else:
                        dischargeDelay = "MANUAL"
                    if preloadSet == "ON":
                        preloadSet = "AUTO"
                    else:
                        preloadSet = "MANUAL"
                    # save results of control panel
                    setData = {
                        "solcast": solcast,
                        "preloadSet": preloadSet,
                        "dischargeDelay": dischargeDelay,
                        "setPreload": setPreload,
                        "octopus": octopus,
                        "ssSet": ssSet,
                        "ssExport": ssExport,
                        "sHrs": sHrs,
                        "sMins": sMins,
                        "fStartHrs": fStartHrs,
                        "fStartMins": fStartMins,
                        "fEndHrs": fEndHrs,
                        "fEndMins": fEndMins,
                        "freeSet": freeSet,
                        "freeDone": freeDone,
                        "boostMode": boostMode,
                        "boostStartHrs": boostStartHrs,
                        "boostStartMins": boostStartMins,
                        "boostEndHrs": boostEndHrs,
                        "boostEndMins": boostEndMins,
                        "boost": boost,
                        "limit": limit,
                        "perm": perm,
                    }
                    setDataJson = json.dumps(setData)
                    f = open("set_bak.json", "w")
                    f.write(setDataJson)
                    f.close()

                # Open Boost dialogue
                if (m.x > 0) and (m.x < 70) and (m.y > 350) and (m.y < 480):
                    watch = 0
                    (
                        boostMode,
                        boostStartHrs,
                        boostStartMins,
                        boostEndHrs,
                        boostEndMins,
                        boost,
                        limit,
                        perm,
                    ) = Boost2.boost(
                        boostMode,
                        boostStartHrs,
                        boostStartMins,
                        boostEndHrs,
                        boostEndMins,
                        boost,
                        int(y[18]),
                        limit,
                        perm,
                        win,
                    )
                    watch = 1
                    if boost == 0:
                        boostStartHrs = 24
                        boostStartMins = 0
                        boostEndHrs = int(nowTime.strftime("%H"))
                        boostEndMins = int(nowTime.strftime("%M"))
                    setData = {
                        "solcast": solcast,
                        "preloadSet": preloadSet,
                        "dischargeDelay": dischargeDelay,
                        "setPreload": setPreload,
                        "octopus": octopus,
                        "ssSet": ssSet,
                        "ssExport": ssExport,
                        "sHrs": sHrs,
                        "sMins": sMins,
                        "fStartHrs": fStartHrs,
                        "fStartMins": fStartMins,
                        "fEndHrs": fEndHrs,
                        "fEndMins": fEndMins,
                        "freeSet": freeSet,
                        "freeDone": freeDone,
                        "boostMode": boostMode,
                        "boostStartHrs": boostStartHrs,
                        "boostStartMins": boostStartMins,
                        "boostEndHrs": boostEndHrs,
                        "boostEndMins": boostEndMins,
                        "boost": boost,
                        "limit": limit,
                        "perm": perm,
                    }
                    setDataJson = json.dumps(setData)
                    f = open("set_bak.json", "w")
                    f.write(setDataJson)
                    f.close()

                if (m.x > 730) and (m.x < 800) and (m.y > 410) and (m.y < 480):
                    watch = 0
                    win.master.state(newstate="iconic")

        wait = 0

        # Display error messages
        oldFail = 0
        if fail == 1:
            display("Unable to contact inverter", "red")
            oldFail = 1
        if fail >= 6:
            display("Too many failures contacting inverter", "red")
            oldFail = 1
        if (fail == 0) and (oldFail == 1):
            display("", "blue")
        if pMessage != None:
            display(pMessage, "blue")
        else:
            messageErased = 0

        cut = re.search("type", invReturn)
        if cut == None:
            continue
        cut = cut.start()
        y = invReturn[cut + 6 : cut + 8]
        if y != "15":
            display("Wrong type of inverter", "red")
            time.sleep(30)
            break

        cut = re.search("Data", invReturn)
        cut = cut.start()
        y = invReturn[cut + 7 :]
        array = re.split(",", y)
        y = array
        if (y[10] == 3) or (y[10] == 4):
            display("Inverter fault","red")
            time.sleep(30)
            continue

        if messageErased != 1:
            rect = Rectangle(Point(64, 350), Point(800, 400))
            rect.setFill("Light Gray")
            rect.setOutline("Light Gray")
            rect.draw(win, 0)
            messageErased = 1
            solDone = 0

        total = int(y[8]) + int(y[9])
        q = datetime.datetime.now()
        ntime = str(q.strftime("%X"))
        feedpower = float(y[32])

        #  convert from twos complement for negative numbers
        if feedpower > 32768:
            gridPower = 256 * 256 - feedpower
            feedpower = 0
        else:
            gridPower = 0
        batpower = float(y[16])
        batpower = 256 * 256 - batpower
        if batpower > 32000:
            batpower = -(256 * 256 - batpower)
        if batpower < 0:
            chargepower = -batpower
            batpower = 0
        else:
            chargepower = 0

        oldmode = mode

        # calculate battery efficiency
        if ((int(y[22]) * 65536) + int(y[21])) != 0:
            efficiency = (
                ((int(y[20]) * 65536) + int(y[19]))
                / ((int(y[22]) * 65536) + int(y[21]))
                * 100
            )
        else:
            efficiency = 80

        # create pointer for charge power
        if (chargepower > 0) and (chargepower > feedpower):
            if chargepower > (Settings.scale * 1000):
                chargepower = Settings.scale * 1000
            mode = "charge"
            pcchargepower = chargepower / 100

        # create pointer for battery power
        elif batpower > 0:
            if batpower > (Settings.scale * 1000):
                batpower = Settings.scale * 1000
            mode = "bat"
            pcbatpower = batpower / 100

        # create pointer for feed to grid
        elif (feedpower > 0) and (feedpower > chargepower):
            if feedpower > (Settings.scale * 1000):
                feedpower = Settings.scale * 1000
            mode = "feed"
            pcfeedpower = feedpower / 100

        else:
            mode = "none"

        # clear pointers if relevant
        if int(total / 100) != int(oldtotal / 100):
            pcoldtotal = oldtotal / 100
            unpointer = Line(
                Point(pointstartx[int(pcoldtotal)], pointstarty[int(pcoldtotal)]),
                Point(pointendx[int(pcoldtotal)], pointendy[int(pcoldtotal)]),
            )
            unpointer.setOutline("yellow")
            unpointer.setWidth(8)
            unpointer.draw(win, 0)

        if (
            (
                (int(chargepower / 100) != int(oldcharge / 100))
                and (int(oldcharge / 100) >= 0)
            )
            or (chargepower == 0)
            or (feedpower > chargepower)
        ):
            pcoldcharge = oldcharge / 100
            unchargepointer = Line(
                Point(pointstartx[int(pcoldcharge)], pointstarty[int(pcoldcharge)]),
                Point(pointendx[int(pcoldcharge)], pointendy[int(pcoldcharge)]),
            )
            unchargepointer.setOutline("yellow")
            unchargepointer.setWidth(8)
            unchargepointer.draw(win, 0)

        if (
            (int(feedpower / 100) != int(oldfeedpower / 100))
            and (int(oldfeedpower / 100) >= 0)
        ) or (feedpower == 0):
            pcoldfeedpower = oldfeedpower / 100
            unfeedpointer = Line(
                Point(
                    pointstartx[int(pcoldfeedpower)], pointstarty[int(pcoldfeedpower)]
                ),
                Point(pointendx[int(pcoldfeedpower)], pointendy[int(pcoldfeedpower)]),
            )
            unfeedpointer.setOutline("yellow")
            unfeedpointer.setWidth(8)
            unfeedpointer.draw(win, 0)

        if (
            (int(batpower / 100) != int(oldbatpower / 100))
            and (int(oldbatpower / 100) >= 0)
        ) or (batpower == 0):
            pcoldbatpower = oldbatpower / 100
            unbatpointer = Line(
                Point(pointstartx[int(pcoldbatpower)], pointstarty[int(pcoldbatpower)]),
                Point(pointendx[int(pcoldbatpower)], pointendy[int(pcoldbatpower)]),
            )
            unbatpointer.setOutline("yellow")
            unbatpointer.setWidth(8)
            unbatpointer.draw(win, 0)

        # write pointer for charge power
        if mode == "charge":
            chargepointer = Line(
                Point(pointstartx[int(pcchargepower)], pointstarty[int(pcchargepower)]),
                Point(pointendx[int(pcchargepower)], pointendy[int(pcchargepower)]),
            )
            chargepointer.setOutline("Green")
            chargepointer.setWidth(8)
            chargepointer.draw(win, 0)

        # write pointer for battery power
        if mode == "bat":
            batpointer = Line(
                Point(pointstartx[int(pcbatpower)], pointstarty[int(pcbatpower)]),
                Point(pointendx[int(pcbatpower)], pointendy[int(pcbatpower)]),
            )
            batpointer.setOutline("Blue")
            batpointer.setWidth(8)
            batpointer.draw(win, 0)

        # write pointer for feed to grid
        if mode == "feed":
            feedpointer = Line(
                Point(pointstartx[int(pcfeedpower)], pointstarty[int(pcfeedpower)]),
                Point(pointendx[int(pcfeedpower)], pointendy[int(pcfeedpower)]),
            )
            feedpointer.setOutline("Red")
            feedpointer.setWidth(8)
            feedpointer.draw(win, 0)

        if mode != oldmode:
            # remove text
            rect = Rectangle(Point(0, 305), Point(400, 350))
            rect.setFill("Light Gray")
            rect.setOutline("Light Gray")
            rect.draw(win, 0)

        if mode == "bat":
            text = Text(Point(200, 320), "Battery power")
            text.setOutline("Blue")
            text.draw(win, 0)
        elif mode == "feed":
            text = Text(Point(200, 320), "Power to grid")
            text.setOutline("Red")
            text.draw(win, 0)
        elif mode == "charge":
            text = Text(Point(200, 320), "Charging")
            text.setOutline("Green")
            text.draw(win, 0)

        # create pointer for PV Power
        if total > (Settings.scale * 1000):
            total = Settings.scale * 1000
        pctotal = total / 100

        # draw pointer for PV power
        pointer = Line(
            Point(pointstartx[int(pctotal)], pointstarty[int(pctotal)]),
            Point(pointendx[int(pctotal)], pointendy[int(pctotal)]),
        )
        pointer.setOutline("Black")
        pointer.setWidth(8)
        pointer.draw(win, 0)

        # display state of charge
        rect = Rectangle(Point(490, 100), Point(580, 300 - (int(y[18]) * 2)))
        rect.setFill("White")
        rect.setOutline("Black")
        rect.draw(win, 0)

        rect = Rectangle(Point(490, 300 - (int(y[18]) * 2)), Point(580, 300))
        rect.setFill("Blue")
        rect.setOutline("Blue")
        rect.draw(win, 0)

        # accumulate solar radiation total
        solarYield = solarYield + (total / 240000)
        # accumulate battery outpout total
        batteryUse = batteryUse + (batpower / 240000)
        # accumulate export power
        export = export + feedinenergy - oldFeedEnergy
        exportGrid = exportGrid + (feedpower / 240000)
        if export > exportGrid:
            exportGrid = export
        # accumulate grid power
        if dayGood == 1:
            dayGrid = dayGrid + (gridPower / 240000)
        elif nightGood == 1:
            nightGrid = nightGrid + (gridPower / 240000)

        if (float(y[32]) < 1) and (feed == 1):
            feed = 0

        if feedinenergy != 0:
            oldFeedEnergy = feedinenergy
        else:
            oldFeedEnergy = 0

        consumeenergy = (int(y[37]) * 256 * 256 + int(y[36])) / 100

        feedinenergy = (int(y[35]) * 256 * 256 + int(y[34])) / 100
        yieldtotal = (int(y[12]) * 256 * 256 + int(y[11])) / 10

        if firstPass == 0:
            oldFeedEnergy = feedinenergy
            firstPass = 1

        localTime = datetime.datetime.now()
        if Settings.timeZone.upper() == "UTC":
            nowTime = datetime.datetime.utcnow()
        else:
            nowTime = localTime

        # set current time to time in minutes
        plusTime = nowTime + datetime.timedelta(hours=12)
        nowTimeMins = ((int(plusTime.strftime("%H"))) * 60) + int(
            nowTime.strftime("%M")
        )

        if nowTimeMins == Settings.startCheapRate:
            nightStart = float(consumeenergy)
            nightGrid = 0
            nightGood = 1
            noFile = 0
            solDone = 0
            octDone = 0
            usedFailed = 1

        # display clock
        if Settings.run.upper() == "AUTO":
            ohrs, omins = dispclk(
                nowTime.strftime("%H"), nowTime.strftime("%M"), ohrs, omins
            )

        # erase preload message
        if (int(nowTime.strftime("%H")) == 1) and (int(nowTime.strftime("%M")) == 0):
            rect = Rectangle(Point(64, 350), Point(800, 400))
            rect.setFill("Light Gray")
            rect.setOutline("Light Gray")
            rect.draw(win, 0)
            pMessage = None

        if nowTimeMins == Settings.endCheapRate:
            currentDate = int(localTime.strftime("%d"))
            setDate = currentDate  # only update date at start of daytime period
            dateError = 0
            dayStart = float(consumeenergy)
            dayGood = 1
            startDayUsed = (
                float(consumeenergy) + float(yieldtotal) - float(feedinenergy)
            )
            usedFailed = 2
            lastNightUsed = nightGrid
            dayGrid = 0
            octDone = 0

        if int(nowTime.strftime("%H")) == int(Settings.noDelay):
            # Check for battery delay
            data = "optType=ReadSetData&pwd=" + Settings.inverterPassword
            x = requests.post(inverterAddress, data=data)
            x = x.text
            y = x[1:]
            array = re.split(",", y)
            delayTime = array[dchReg - 1]
            mins = int(int(delayTime) / 256)
            hrs = int(delayTime) - (mins * 256)
            if delayTime != Settings.noDelay:
                delaySet = 1

        # display delay message
        if delaySet == 1:
            if (int(localTime.strftime("%H")) >= int(Settings.noDelay)) and (
                int(localTime.strftime("%H")) < hrs
            ):
        # Checkfor battery delay from inverter
                data = "optType=ReadSetData&pwd=" + Settings.inverterPassword
                x = requests.post(inverterAddress, data=data)
                x = x.text
                y = x[1:]
                array = re.split(",", y)
                delayTime = array[dchReg - 1]
                mins = int(int(delayTime) / 256)
                hrs = int(delayTime) - (mins * 256)
                if mins == 0:
                    tstring = str(hrs)
                else:
                    tstring = str(hrs) + ":" + str(mins + 100)[1:3]
                if (hrs == 12) and (mins == 0):
                    setDelay = "Battery use delayed until " + tstring + " noon"
                elif delayTime == Settings.noDelay:
                    setDelay = ""
                elif hrs < 13:
                    setDelay = "Battery use delayed until " + tstring + " am"
                else:
                    if mins == 0:
                        tstring = str(hrs - 12)
                    else:
                        tstring = str(hrs - 12) + ":" + str(mins + 100)[1:3]
                    setDelay = "Battery use delayed until " + tstring + " pm"
                pMessage = setDelay
                display(pMessage, "blue")
                delaySet = 2

        # Check National Grid website for an Octopus Saving Session
        # These can now work in two ways, creating a Free Session as well as a Saving Session
        if (octopus == "ON") and (octDone == 0):
            if (
                (int(localTime.strftime("%H")) >= 9)
                and (int(localTime.strftime("%H")) < 21)
                and (int(localTime.strftime("%M")) == 5)
                and (int(localTime.strftime("%S")) < 30)
            ):
                ssDelay = Octopus5.check()
                ssSet = ssDelay[1]
                if ssDelay[0] != "":
                    octDone = 2
                    if ssDelay[6] == "Downwards":
                        delaySet = 2
                        sHrs = ssDelay[2]
                        sMins = ssDelay[3]
                        fEndHrs = ssDelay[4]
                        fEndMins = ssDelay[5]
                        if ssDelay[1] != 0:
                            delayTime = set3.set(
                                inverterAddress,
                                Settings.inverterPassword,
                                dchReg,
                                ssDelay[1],
                            )
                            if type(delayTime) == str:
                                octDone = 0
                    elif ssDelay[6] == "Upwards":
                        fStartHrs = ssDelay[2]
                        fStartMins = ssDelay[3]
                        fEndHrs = ssDelay[4]
                        fEndMins = ssDelay[5]
                    if int(localTime.strftime("%H")) < fEndHrs: 
                        pMessage = ssDelay[0]
                        display(pMessage, "blue")

                    setData = {
                        "solcast": solcast,
                        "preloadSet": preloadSet,
                        "dischargeDelay": dischargeDelay,
                        "setPreload": setPreload,
                        "octopus": octopus,
                        "ssSet": ssSet,
                        "ssExport": ssExport,
                        "sHrs": sHrs,
                        "sMins": sMins,
                        "fStartHrs": fStartHrs,
                        "fStartMins": fStartMins,
                        "fEndHrs": fEndHrs,
                        "fEndMins": fEndMins,
                        "freeSet": freeSet,
                        "freeDone": freeDone,
                        "boostMode": boostMode,
                        "boostStartHrs": boostStartHrs,
                        "boostStartMins": boostStartMins,
                        "boostEndHrs": boostEndHrs,
                        "boostEndMins": boostEndMins,
                        "boost": boost,
                        "limit": limit,
                        "perm": perm,
                    }
                    setDataJson = json.dumps(setData)
                    f = open("set_bak.json", "w")
                    f.write(setDataJson)
                    f.close()
                else:
                    octDone = 0

        # set work mode to Forced discharge for Boost function
        if (
            (int(localTime.strftime("%H")) == boostStartHrs)
            and (int(localTime.strftime("%M")) >= boostStartMins)
            and (boost == 1)
        ) or (boost == 2):
            chargeStart, chargeEnd, dischargeStart, dischargeEnd = Info4.getInvTimes(
                inverterAddress
            )
            Info4.saveTimes(chargeStart, chargeEnd, dischargeStart, dischargeEnd)
            rtn = set3.set(inverterAddress, Settings.inverterPassword, modeReg, 0)
            if boostMode > 3:
                rtn = set3.set(inverterAddress, Settings.inverterPassword, modeReg, 3)
                rtn = set3.set(inverterAddress, Settings.inverterPassword, forceReg, 2)
            else:
                set3.set(inverterAddress, Settings.inverterPassword, dchReg, 0)
                set3.set(inverterAddress, Settings.inverterPassword, dchReg + 1, 15127)
            boost = 3
            carCharge = 0
            iMessage = pMessage
            pMessage = "Boost active"
            display(pMessage, "Blue")

        # set work mode to Manual and Forced charge for free session
        if (
            (int(localTime.strftime("%H")) == fStartHrs)
            and (int(localTime.strftime("%M")) >= fStartMins)
            and (freeSet == 1)
        ):
            rtn = set3.set(inverterAddress, Settings.inverterPassword, modeReg, 3)
            rtn = set3.set(inverterAddress, Settings.inverterPassword, forceReg, 1)
            freeSet = 2
            freeDone = 1
            carCharge = 0
            pMessage = "Free power session"

        # set work mode back to self use after free session or saving session
        if (
            (int(localTime.strftime("%H")) >= fEndHrs)
            and (int(localTime.strftime("%M")) >= fEndMins)
            and (freeSet != 0)
            and (freeDone == 1)
        ):
            ssActive = 0
            chargeStart, chargeEnd, dischargeStart, dischargeEnd = Info4.getTimes()
            rtn = set3.set(inverterAddress, Settings.inverterPassword, modeReg, 0)
            set3.set(inverterAddress, Settings.inverterPassword, dchReg, dischargeStart)
            set3.set(
                inverterAddress, Settings.inverterPassword, dchReg + 1, dischargeEnd
            )
            freeSet = 0
            freeDone = 0
            rect = Rectangle(Point(64, 350), Point(800, 400))
            rect.setFill("Light Gray")
            rect.setOutline("Light Gray")
            rect.draw(win, 0)
            pMessage = None
            offset = Settings.offset
            octDone = 0

        # set work mode back to self use after Boost complete
        if (
            (
                (int(localTime.strftime("%H")) >= boostEndHrs)
                and (int(localTime.strftime("%M")) >= boostEndMins)
                and (boost == 3)
            )
            or (boost == 4)
            or ((boost == 3) and (limit >= int(y[18])))
        ):
            if (boostMode > 0) and (limit >= int(y[18])):
                pMessage = "Boost cancelled, discharge limit reached"
            chargeStart, chargeEnd, dischargeStart, dischargeEnd = Info4.getTimes()
            rtn = set3.set(inverterAddress, Settings.inverterPassword, modeReg, 0)
            set3.set(inverterAddress, Settings.inverterPassword, dchReg, dischargeStart)
            set3.set(
                inverterAddress, Settings.inverterPassword, dchReg + 1, dischargeEnd
            )
            rect = Rectangle(Point(64, 350), Point(800, 400))
            rect.setFill("Light Gray")
            rect.setOutline("Light Gray")
            rect.draw(win, 0)
            if (int(localTime.strftime("%H")) >= boostEndHrs) and (
                int(localTime.strftime("%M")) >= boostEndMins
            ):
                pMessage = iMessage
            if pMessage != None:
                display(pMessage, "Blue")
            if perm == "OFF":
                boost = 0
                boostMode = 0
                limit = 10
            else:
                boost = 1
            setData = {
                "solcast": solcast,
                "preloadSet": preloadSet,
                "dischargeDelay": dischargeDelay,
                "setPreload": setPreload,
                "octopus": octopus,
                "ssSet": ssSet,
                "ssExport": ssExport,
                "sHrs": sHrs,
                "sMins": sMins,
                "fStartHrs": fStartHrs,
                "fStartMins": fStartMins,
                "fEndHrs": fEndHrs,
                "fEndMins": fEndMins,
                "freeSet": freeSet,
                "freeDone": freeDone,
                "boostMode": boostMode,
                "boostStartHrs": boostStartHrs,
                "boostStartMins": boostStartMins,
                "boostEndHrs": boostEndHrs,
                "boostEndMins": boostEndMins,
                "boost": boost,
                "limit": limit,
                "perm": perm,
            }
            setDataJson = json.dumps(setData)
            f = open("set_bak.json", "w")
            f.write(setDataJson)
            f.close()

        # set work mode to Manual and Forced discharge for Saving Session
        if (
            (int(localTime.strftime("%H")) == sHrs)
            and (int(localTime.strftime("%M")) == sMins)
            and (octDone == 2)
        ):
            ssActive = 1
            if ssExport.upper == "YES":
                rtn = set3.set(inverterAddress, Settings.inverterPassword, modeReg, 3)
                rtn = set3.set(inverterAddress, Settings.inverterPassword, forceReg, 2)
            else:
                (
                    chargeStart,
                    chargeEnd,
                    dischargeStart,
                    dischargeEnd,
                ) = Info4.getInvTimes(inverterAddress)
                Info4.saveTimes(chargeStart, chargeEnd, dischargeStart, dischargeEnd)
                rtn = set3.set(inverterAddress, Settings.inverterPassword, modeReg, 0)
                set3.set(inverterAddress, Settings.inverterPassword, dchReg, 0)
                set3.set(inverterAddress, Settings.inverterPassword, dchReg + 1, 15127)
                freeSet = 2
                freeDone = 1
                carCharge = 0
                pMessage = "Saving session"

        # erase delay Octopus message and reset work mode to Self Use
        if (
            (int(localTime.strftime("%H")) == hrs)
            and (int(localTime.strftime("%M")) == mins)
            and (delaySet == 2)
        ):
            ssActive = 0
            if octDone == 2:
                chargeStart, chargeEnd, dischargeStart, dischargeEnd = Info4.getTimes()
                rtn = set3.set(inverterAddress, Settings.inverterPassword, modeReg, 0)
                set3.set(
                    inverterAddress, Settings.inverterPassword, dchReg, dischargeStart
                )
                set3.set(
                    inverterAddress, Settings.inverterPassword, dchReg + 1, dischargeEnd
                )
            rect = Rectangle(Point(64, 350), Point(800, 400))
            rect.setFill("Light Gray")
            rect.setOutline("Light Gray")
            rect.draw(win, 0)
            delaySet = 0
            octDone = 3
            pMessage = None

        # get tomorrow's likely useage from file
        if (int(localTime.strftime("%H")) == 15) and (
            int(localTime.strftime("%M")) == 0
        ):
            endDayUsed = float(consumeenergy) + float(yieldtotal) - float(feedinenergy)
            todayUsed = endDayUsed - startDayUsed
            logDone = 0
            noFile = 0
            if dateError == 0:
                tomUsed = Week2.means(todayUsed)
            if usedFailed == 2:
                usedFailed = 0

        # run Solcast process
        if solcast == "ON":
            if (int(localTime.strftime("%H")) >= 21) and (solDone != 1):
                preload = Solcast4.getForecast(tomUsed, efficiency)
                if type(preload) == str:
                    pMessage = preload
                else:
                    setPreload = preload
                    if setPreload > 95:
                        setPreload = 95
                    if setPreload > 10:
                        pMessage = (
                            "Recommended preload for tonight is "
                            + str(setPreload)
                            + "%"
                        )
                    else:
                        setPreload = 10
                        pMessage = "No recommended preload tonight"
                    solDone = 1
                display(pMessage, "blue")

                if type(preload) != str:
                    # set battery overnight preload
                    if (preloadSet == "AUTO") and (type(preload) == int):
                        setPreload = preload + offset
                        if setPreload > 95:
                            setPreload = 95
                        elif setPreload < (offset + 10):
                            setPreload = offset + 10
                        setPreload = set3.set(
                            inverterAddress,
                            Settings.inverterPassword,
                            chgReg,
                            setPreload,
                        )
                        if type(setPreload) == str:
                            pMessage = setPreload
                        else:
                            pMessage = "Preload is set to " + str(setPreload) + "%"
                        display(pMessage, "blue")
                        solDone = 1

                    # work out and set discharge delay
                    if (dischargeDelay == "AUTO") and (type(setPreload) != str):
                        time.sleep(10)
                        upreload = preload + offset
                        if upreload > 95:
                            overLoad = upreload - 95
                            delay = int(overLoad * 8 / 100)
                            if delay > 8:
                                delay = 8
                            delayTime = set3.set(
                                inverterAddress,
                                Settings.inverterPassword,
                                dchReg,
                                delay + Settings.noDelay,
                            )
                            delaySet = 1
                        else:
                            delayTime = set3.set(
                                inverterAddress,
                                Settings.inverterPassword,
                                dchReg,
                                Settings.noDelay,
                            )
                            delaySet = 0
                        if type(delayTime) == str:
                            delayTime = Settings.noDelay
                            pMessage = "Discharge time not set"
                            display(pMessage, "blue")

        if (exportGrid > 0) and (exportGrid != oldExportGrid):
            rect = Rectangle(Point(340, 240), Point(460, 260))
            rect.setFill("Light Gray")
            rect.setOutline("Light Gray")
            rect.draw(win, 0)
            time.sleep(0.04)
            text = Text(Point(400, 250), str(round(exportGrid, 2)) + " kWh")
            text._reconfig("font", ("Arial", 18, "normal"))
            text.draw(win, 0)

        if noFile == 0:
            if nightGood == 1:
                if (nowTimeMins >= Settings.startCheapRate) and (
                    nowTimeMins < Settings.endCheapRate
                ):
                    nightUsed = int((consumeenergy - nightStart) * 100) / 100
                else:
                    nightGood = 0
                if oldNightGrid != nightGrid:
                    rect = Rectangle(Point(620, 240), Point(800, 260))
                    rect.setFill("Light Gray")
                    rect.setOutline("Light Gray")
                    rect.draw(win, 0)
                    time.sleep(0.04)
                    text = Text(Point(680, 250), str(round(nightGrid, 2)) + " kWh")
                    text._reconfig("font", ("Arial", 18, "normal"))
                    text.draw(win, 0)
                    oldNightUsed = nightUsed
                    oldNightGrid = nightGrid

            if dayGood == 1:
                if not (
                    (nowTimeMins >= Settings.startCheapRate)
                    and (nowTimeMins < Settings.endCheapRate)
                ):
                    dayUsed = int((consumeenergy - dayStart) * 100) / 100
                else:
                    dayGood = 0
                if oldDayGrid != dayGrid:
                    rect = Rectangle(Point(620, 140), Point(800, 160))
                    rect.setFill("Light Gray")
                    rect.setOutline("Light Gray")
                    rect.draw(win, 0)
                    text = Text(Point(680, 150), str(round(dayGrid, 2)) + " kWh")
                    text._reconfig("font", ("Arial", 18, "normal"))
                    text.draw(win, 0)
                    oldDayUsed = dayUsed
                    oldDayGrid = dayGrid

        # Change source if counted data is wrong
        if dayUsed > dayGrid:
            dayGrid = dayUsed
        if nightUsed > nightGrid:
            nightGrid = nightUsed

        # Logic to prevent car charging using power from the batteries
        # if power exceeds a threshold for more than a set time, block battery discharge
        if (Settings.EVmode.upper() == "YES") and (boost < 3) and (ssActive == 0) and (invMode == "0") and (freeSet < 2):
            carThreshold = Settings.carThreshold
            carDelay = Settings.carDelay
            consume = int(y[38])
            if dayGood == 1:
                if (consume >= carThreshold) and (oldConsume < carThreshold):
                    carStart = nowTimeMins
                if (carCharge == 0) and (consume >= carThreshold) and (nowTimeMins > (carStart + carDelay)):
                    carCharge = 1
                elif (consume < carThreshold) and (carCharge < 2):
                    carCharge = 0
                if carCharge == 1:
                    carCharge = 2
                    (
                        chargeStart,
                        chargeEnd,
                        dischargeStart,
                        dischargeEnd,
                    ) = Info4.getInvTimes(inverterAddress)
                    
                    Info4.saveTimes(chargeStart,chargeEnd,dischargeStart,dischargeEnd)
                    Info4.sendInvMode(inverterAddress,win,selfMode)
                    Info4.sendInvTimes(inverterAddress,win,chargeStart,chargeEnd,0,0)
                    pMessage = "Battery turned off due to car charging"
                    display(pMessage,"Blue")

            # Return to normal if carCharging has ended
            if (carCharge == 2) and (consume < carThreshold):
                carCharge = 0
                chargeStart, chargeEnd, dischargeStart, dischargeEnd = Info4.getTimes()
                rtn = set3.set(inverterAddress, Settings.inverterPassword, modeReg, 0)
                set3.set(
                    inverterAddress, Settings.inverterPassword, dchReg, dischargeStart
                )
                set3.set(
                    inverterAddress, Settings.inverterPassword, dchReg + 1, dischargeEnd
                )
                rect = Rectangle(Point(64, 350), Point(800, 400))
                rect.setFill("Light Gray")
                rect.setOutline("Light Gray")
                rect.draw(win, 0)
                pMessage = None
                
            oldConsume = consume

        oldfeedpower = feedpower
        oldbatpower = batpower
        oldtotal = total
        oldcharge = chargepower
        oldDayUsed = dayUsed
        oldExportGrid = exportGrid
        oldGridPower = gridPower

        # Save localData
        if ((float(y[32]) != oldFeedIn) or (gridPower != 0)) and (dateError == 0):
            localData = {
                "Date": setDate,
                "nightStart": nightStart,
                "nightUsed": nightUsed,
                "dayStart": dayStart,
                "dayUsed": dayUsed,
                "startDayUsed": startDayUsed,
                "endDayUsed": endDayUsed,
                "todayUsed": todayUsed,
                "tomUsed": tomUsed,
                "efficiency": efficiency,
                "solarYield": solarYield,
                "batteryUse": batteryUse,
                "dayGrid": dayGrid,
                "nightGrid": nightGrid,
                "export": export,
                "exportGrid": exportGrid,
            }
            localDataJson = json.dumps(localData)
            f = open("power.json", "w")
            f.write(localDataJson)
            f.close()
            oldFeedIn = y[32]

        if feedpower < 0:
            feedpower = 0

        # Send data to log
        if (
            (Settings.log.upper() == "YES")
            and (logDone == 0)
            and (nowTimeMins == Settings.startCheapRate)
        ):
            logDone = powerLog.logPower(
                round(dayGrid, 2), lastNightUsed, solarYield, batteryUse, exportGrid
            )
            if logDone == 1:
                solarYield = 0
                batteryUse = 0
                export = 0
                exportGrid = 0
                feedpower = 0
                oldfeedpower = 1

except Exception as e:
    errLog(e)
    if Settings.run.upper() == "AUTO":
        watch = 2
    else:
        raise
