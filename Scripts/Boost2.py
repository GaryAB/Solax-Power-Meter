from graphics import *
import time
import datetime
import json
import SetTimes
import Settings
import requests
import re
import set3
from Info3 import switchOn, switchOff, toggle
from Info3 import makeButton, touch, untouch

dchReg = 39 #Register to set discharge start time
chgReg = 31 #Register to set charge limit
modeReg = 28 #Register to set working mode
manReg = 36 #Register to adjust manual mode
selfMode = 0 #Setting for Self Use mode
manualMode = 3 #Setting for Manual mode
forceCharge = 1 #Setting for manual mode force charge
forceDischarge = 2 #Setting for manual mode force discharge

# boost settings
# boost = 0: Boost disabled
# boost = 1: Boost preset
# boost = 2: Activate boot
# boost = 3: Boost activated
# boost = 4: Abort boost

#Boost modes
#boostMode = 1:30 minute boost
#boostMode = 2:1 hour boost
#boostMode = 3:Timed boost
#boostMode = 4:30 minute boost and export
#boostMode = 5:1 hour boost and export
#boostMode = 6:Timed boost and export


def boost(boostMode, boostStartHrs,boostStartMins,boostEndHrs,boostEndMins,boost,SOC,limit,perm,win):

    newLimit = limit

    halfButton = "OFF"
    fullButton = "OFF"
    timeButton = "OFF"
    halfExport = "OFF"
    fullExport = "OFF"
    timeExport = "OFF"
    new = 0
    if boostMode == 1:
        halfButton = "ON"
    elif boostMode == 2:
        fullButton = "ON"
    elif boostMode == 3:
        timeButton = "ON"
    elif boostMode == 4:
        halfExport = "ON"
    elif boostMode == 5:
        fullExport = "ON"
    elif boostMode == 6:
        timeExport = "ON"
    
    boostWin = GraphWin("Boost",600,410)

    rect = Rectangle(Point(0,0), Point(600,410))
    rect.setFill('light gray')
    rect.draw(boostWin)

# Return button
    rect = Rectangle(Point(250,350), Point(350,390))
    rect.setFill("White")
    rect.setOutline('Black')
    rect.draw(boostWin)

# button labels
    text = Text(Point(300,25),'Boost')
    text._reconfig("font",("Arial",14,"bold"))
    text.draw(boostWin)

    text = Text(Point(300,153),'Boost and Export')
    text._reconfig("font",("Arial",14,"bold"))
    text.draw(boostWin)

    text = Text(Point(300,258),'Discharge Limit')
    text._reconfig("font",("Arial",14,"bold"))
    text.draw(boostWin)

    text = Text(Point(150,55),'Half hour')
    text._reconfig("font",("Arial",12,"bold"))
    text.draw(boostWin)

    text = Text(Point(300,55),'1 hour')
    text._reconfig("font",("Arial",12,"bold"))
    text.draw(boostWin)

    text = Text(Point(450,55),'Timed')
    text._reconfig("font",("Arial",12,"bold"))
    text.draw(boostWin)

    text = Text(Point(300,370),'Return')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(boostWin)

#Switch label

    text = Text(Point(450,370),'Permanent')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(boostWin)


#30 sec button
    if halfButton == 'ON':
        makeButton(boostWin,150,100,'Blue')
    else:
        makeButton(boostWin,150,100,'White')

#1 hour button
    if fullButton == 'ON':
        makeButton(boostWin,300,100,'Blue')
    else:
        makeButton(boostWin,300,100,'White')

#Timed button
    if timeButton == 'ON':
        makeButton(boostWin,450,100,'Blue')
    else:
        makeButton(boostWin,450,100,'White')

#30 sec export
    if halfExport == 'ON':
        makeButton(boostWin,150,205,'Red')
    else:
        makeButton(boostWin,150,205,'White')

#1 hour export
    if fullExport == 'ON':
        makeButton(boostWin,300,205,'Red')
    else:
        makeButton(boostWin,300,205,'White')

#Timed export
    if timeExport == 'ON':
        makeButton(boostWin,450,205,'Red')
    else:
        makeButton(boostWin,450,205,'White')

#Draw initial slider
    if perm == "OFF":
        limit = SOC
    drawSlider(1,0,boostWin)
    drawLimit(SOC,limit,boostWin)

#Permanent switch
    if perm == 'ON':
        switchOn(boostWin,540,370,'Green')
    else:
        switchOff(boostWin,540,370)

    try:
        while True:
            # set current date and time  
            localTime = datetime.datetime.now()
            if Settings.timeZone.upper() == "UTC":
                nowTime= datetime.datetime.utcnow()
            else:
                nowTime = localTime

    # Mouse click on master window
            m = win.checkMouse()
            if m != None:
                boostWin.close()
                return boostMode, boostStartHrs, boostStartMins, boostEndHrs, boostEndMins, boost, newLimit, perm

    # Return pressed
            m = boostWin.checkMouse()
            if m != None:
                if (m.x > 250) and (m.x < 350) and (m.y > 350) and (m.y < 390):
                    boostWin.close()
                    return boostMode, boostStartHrs, boostStartMins, boostEndHrs, boostEndMins, boost, newLimit, perm

    # 30 minute button pressed
                x = 150
                y = 100
                if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                    if boostMode == 1:
                        boost = 4
                        boostMode = 0
                        limit = 10
                        halfButton = untouch (boostWin,x,y)
                        drawLimit(SOC,limit,boostWin)
                    else:
                        halfButton = touch(boostWin,x,y,'Blue')
                        fullButton = untouch(boostWin,300,100)
                        timeButton = untouch(boostWin,450,100)
                        halfExport = untouch(boostWin,150,205)
                        fullExport = untouch(boostWin,300,205)
                        timeExport = untouch(boostWin,450,205)
                        boostStart = nowTime + datetime.timedelta(minutes = 1)
                        boostEnd = boostStart + datetime.timedelta(minutes = 30)
                        boostStartHrs = int(boostStart.strftime("%H"))
                        boostStartMins = int(boostStart.strftime("%M"))
                        boostEndHrs = int(boostEnd.strftime("%H"))
                        boostEndMins = int(boostEnd.strftime("%M"))
                        boost = 2
                        boostMode = 1
                        new = 1
                            
    # 1 hour button pressed
                x = 300
                y = 100
                if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                    if boostMode == 2:
                        boost = 4
                        boostMode = 0
                        limit = 10
                        fullButton = untouch (boostWin,x,y)
                        drawLimit(SOC,limit,boostWin)
                    else:
                        fullButton = touch(boostWin,x,y,'Blue')
                        halfButton = untouch(boostWin,150,100)
                        timeButton = untouch(boostWin,450,100)
                        halfExport = untouch(boostWin,150,205)
                        fullExport = untouch(boostWin,300,205)
                        timeExport = untouch(boostWin,450,205)
                        boostStart = nowTime + datetime.timedelta(minutes = 1)
                        boostEnd = boostStart + datetime.timedelta(hours = 1)
                        boostStartHrs = int(boostStart.strftime("%H"))
                        boostStartMins = int(boostStart.strftime("%M"))
                        boostEndHrs = int(boostEnd.strftime("%H"))
                        boostEndMins = int(boostEnd.strftime("%M"))
                        boost = 2
                        boostMode = 2
                        new = 1
                        
    # Timed button pressed
                x = 450
                y = 100
                if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                    if boostMode == 3:
                        boost = 4
                        boostMode = 0
                        limit = 10
                        timeButton = untouch (boostWin,x,y)
                        drawLimit(SOC,limit,boostWin)
                    else:
                        timeButton = touch(boostWin,x,y,'Blue')
                        halfButton = untouch(boostWin,150,100)
                        fullButton = untouch(boostWin,300,100)
                        halfExport = untouch(boostWin,150,205)
                        fullExport = untouch(boostWin,300,205)
                        timeExport = untouch(boostWin,450,205)
                        if boost != 4: 
                            boostStart = nowTime
                            boostEnd = boostStart + datetime.timedelta(hours = 1)
                            boostStartHrs = int(boostStart.strftime("%H"))
                            boostStartMins = int(boostStart.strftime("%M"))
                            boostEndHrs = int(boostEnd.strftime("%H"))
                            boostEndMins = int(boostEnd.strftime("%M"))
                        boostStartHrs, boostStartMins, boostEndHrs, boostEndMins = SetTimes.setTimes(boostStartHrs, boostStartMins, boostEndHrs, boostEndMins, "Boost Period", win, boostWin)
                        boost = 1
                        boostMode = 3

      
                
    # 30 minute export pressed
                x = 150
                y = 205
                if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                    if boostMode == 4:
                        boost = 4
                        boostMode = 0
                        limit = 10
                        halfExport = untouch (boostWin,x,y)
                        drawLimit(SOC,limit,boostWin)
                    else:
                        halfExport = touch(boostWin,x,y,'Red')
                        halfButton = untouch(boostWin,150,100)
                        fullButton = untouch(boostWin,300,100)
                        timeButton = untouch(boostWin,450,100)
                        fullExport = untouch(boostWin,300,205)
                        timeExport = untouch(boostWin,450,205)
                        boostStart = nowTime + datetime.timedelta(minutes = 1)
                        boostEnd = boostStart + datetime.timedelta(minutes = 30)
                        boostStartHrs = int(boostStart.strftime("%H"))
                        boostStartMins = int(boostStart.strftime("%M"))
                        boostEndHrs = int(boostEnd.strftime("%H"))
                        boostEndMins = int(boostEnd.strftime("%M"))
                        boost = 2
                        boostMode = 4
                        new = 1
                            
    # 1 hour export pressed
                x = 300
                y = 205
                if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                    if boostMode == 5:
                        boost = 4
                        boostMode = 0
                        limit = 10
                        fullEXport = untouch (boostWin,x,y)
                        drawLimit(SOC,limit,boostWin)
                    else:
                        fullExport = touch(boostWin,x,y,'Red')
                        halfButton = untouch(boostWin,150,100)
                        fullButton = untouch(boostWin,300,100)
                        timeButton = untouch(boostWin,450,100)
                        halfExport = untouch(boostWin,150,205)
                        timeExport = untouch(boostWin,450,205)
                        boostStart = nowTime + datetime.timedelta(minutes = 1)
                        boostEnd = boostStart + datetime.timedelta(hours = 1)
                        boostStartHrs = int(boostStart.strftime("%H"))
                        boostStartMins = int(boostStart.strftime("%M"))
                        boostEndHrs = int(boostEnd.strftime("%H"))
                        boostEndMins = int(boostEnd.strftime("%M"))
                        boost = 2
                        boostMode = 5
                        new = 1
                        
    # Timed export pressed
                x = 450
                y = 205
                if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                    if boostMode == 6:
                        boost = 4
                        boostMode = 0
                        limit = 10
                        timeExport = untouch (boostWin,x,y)
                        drawLimit(SOC,limit,boostWin)
                    else:
                        timeExport = touch(boostWin,x,y,'Red')
                        halfButton = untouch(boostWin,150,100)
                        fullButton = untouch(boostWin,300,100)
                        timeButton = untouch(boostWin,450,100)
                        halfExport = untouch(boostWin,150,205)
                        fullExport = untouch(boostWin,300,205)
                        if boost != 4: 
                            boostStart = nowTime
                            boostEnd = boostStart + datetime.timedelta(hours = 1)
                            boostStartHrs = int(boostStart.strftime("%H"))
                            boostStartMins = int(boostStart.strftime("%M"))
                            boostEndHrs = int(boostEnd.strftime("%H"))
                            boostEndMins = int(boostEnd.strftime("%M"))
                        boostStartHrs, boostStartMins, boostEndHrs, boostEndMins = SetTimes.setTimes(boostStartHrs, boostStartMins, boostEndHrs, boostEndMins, "Boost Period", win, boostWin)
                        boost = 1
                        boostMode = 6

     # Permanent switch pressed
                x = 540
                y = 370
                if (m.x > x-38) and (m.x < x+38) and (m.y > y-8) and (m.y < y+8):
                    perm = toggle(boostWin,x,y,'Green',perm)
                    if perm == "OFF":
                        if newLimit > SOC:
                            newLimit = SOC
                        a = SOC
                        redraw = 1
                        drawSlider(redraw,a,boostWin)
                        drawLimit(SOC,newLimit,boostWin)
                      
     # ser battery discharge limit
                if perm == "ON":
                    max = 100
                else:
                    max = SOC
                    
                if (m.x > 140) and (m.x < 100+max*4) and (m.y > 280) and (m.y < 320):
                    newLimit = (m.x - 100)/4
                    #Draw Battery Limit
                    if SOC > newLimit:
                        a = SOC
                        redraw = 1
                    else:
                        a = newLimit
                        redraw = 1
                    drawSlider(redraw,a,boostWin)
                    drawLimit(SOC,newLimit,boostWin)


    except Exception as e:
        try:
            boostWin.close()
            return (0, boostStartHrs, boostStartMins, boostEndHrs, boostEndMins, 4, newLimit, perm)
        except:
            os.system ('sudo reboot')

def drawSlider(redraw,a,boostWin):
    #Draw battery slider
    if redraw == 1:
        rect = Rectangle(Point(100+a*4, 280), Point(500,320))
        rect.setFill("White")
        rect.setWidth(2)
        rect.setOutline('Black')
        rect.draw(boostWin)

    a = int(a/10)
    while a < 10:
        line = Line(Point((100+a*40),280), Point((100+a*40),320))
        line.setWidth(1)
        line.setOutline('Gray')
        line.draw(boostWin)
        text = Text(Point(100+a*40,330),str(10*a))
        text._reconfig("font",("Arial",10,"normal"))
        text.draw(boostWin)
        text = Text(Point(480,330),"%")
        text._reconfig("font",("Arial",10,"normal"))
        text.draw(boostWin)
        a = a + 1

def drawLimit(SOC,limit,boostWin):
    #Draw Battery Limit
    rect = Rectangle(Point(100, 280), Point((100+limit*4),319))
    rect.setFill("Blue")
    rect.draw(boostWin)

    #Draw battery extent
    if SOC > limit:
        rect = Rectangle(Point((100+limit*4), 280), Point((100+SOC*4),319))
        rect.setFill("Aqua")
        rect.draw(boostWin)
    










