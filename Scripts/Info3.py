from graphics import *
import os
import time
import json
import SetTimes
import Settings
import requests
import re
import set3

dchReg = 39 #Register to set discharge start time
chgReg = 31 #Register to set charge limit
modeReg = 28 #Register to set working mode
manReg = 36 #Register to adjust manual mode
selfMode = 0 #Setting for Self Use mode
manualMode = 3 #Setting for Manual mode
forceCharge = 1 #Setting for manual mode force charge
forceDischarge = 2 #Setting for manual mode force discharge

def info(inverterAddress,solcast,preloadSet,dischargeDelay,setPreload,octopus,freeTag,fStartHrs, fStartMins, fEndHrs, fEndMins, offset, win):

# Reset data
    chargeAuto = 'OFF'
    oldChargeAuto = 'OFF'
    chargeBlock = 'OFF'
    chargeForce = 'OFF'
    dischargeAuto = 'OFF'
    oldDischargeAuto = 'OFF'
    dischargeBlock = 'OFF'
    dischargeForce = 'OFF'
    exportForce = 'OFF'

    chargeStart = 0
    chargeEnd = 0
    dischargeStart = 0
    dischargeEnd = 0

# get mode and times data from inverter
    chargeStart,chargeEnd,dischargeStart,dischargeEnd = getInvTimes(inverterAddress)
    if getInvMode(inverterAddress) == '0': # Inverter in Self Use mode
        if (chargeStart == '0') and (chargeEnd == '0'):
            chargeBlock = 'ON'
        else:
            chargeAuto = 'ON'
            oldChargeAuto = 'ON'
        if (dischargeStart == '0') and (dischargeEnd == '0'):
            dischargeBlock = 'ON'
        else:
            dischargeAuto = 'ON'
            oldDischargeAuto = 'ON'
        if (dischargeStart == '0') and (dischargeEnd == '15127'):
            chargeAuto = 'OFF'
            chargeBlock ='ON'
            dischargeAuto = 'OFF'
            dischargeForce = 'ON'
    elif getInvMode(inverterAddress) == '3': # Inverter in Manual mode
        if getManMode(inverterAddress) == '1': # Forced Charge
            chargeForce = 'ON'
            dischargeBlock = 'ON'
        elif getManMode(inverterAddress) == '2': # Forced Export
            exportForce = 'ON'
            chargeBlock = 'ON'
        chargeAuto = 'OFF'
        dischargeAuto = 'OFF'

# get times data from file if inverter data invalid
    if (chargeAuto.upper() == 'OFF') or (dischargeAuto.upper() == 'OFF'):
        chargeStart, chargeEnd, dischargeStart, dischargeEnd = getTimes()

    infoWin = GraphWin("Control Panel",600,400)

    rect = Rectangle(Point(0,0), Point(600,400))
    rect.setFill('light gray')
    rect.draw(infoWin)

# Return button
    rect = Rectangle(Point(250,350), Point(350,390))
    rect.setFill("White")
    rect.setOutline('Black')
    rect.draw(infoWin)

#solacast switch
    text = Text(Point(100,30),'Solcast')
    text._reconfig("font",("Arial",11,"normal"))
    text.draw(infoWin)

# preload switch
    text = Text(Point(200,30),'Set preload')
    text._reconfig("font",("Arial",11,"normal"))
    text.draw(infoWin)

# delay switch
    text = Text(Point(300,30),'Discharge Delay')
    text._reconfig("font",("Arial",11,"normal"))
    text.draw(infoWin)

# octopus switch
    text = Text(Point(400,30),'Octopus')
    text._reconfig("font",("Arial",11,"normal"))
    text.draw(infoWin)

# free session switch
    text = Text(Point(500,30),'Free Session')
    text._reconfig("font",("Arial",11,"normal"))
    text.draw(infoWin)

# button labels
    text = Text(Point(300,100),'Battery Charging from Grid')
    text._reconfig("font",("Arial",12,"bold"))
    text.draw(infoWin)

    text = Text(Point(100,125),'Auto')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(infoWin)

    text = Text(Point(500,125),'Block')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(infoWin)

    text = Text(Point(430,125),'Force')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(infoWin)

    text = Text(Point(300,230),'Battery Discharging')
    text._reconfig("font",("Arial",12,"bold"))
    text.draw(infoWin)

    text = Text(Point(100,255),'Auto')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(infoWin)

    text = Text(Point(500,255),'Block')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(infoWin)

    text = Text(Point(430,255),'Force')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(infoWin)

    text = Text(Point(360,255),'Export')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(infoWin)

    text = Text(Point(300,370),'Return')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(infoWin)



# Solcast switch
    if solcast == 'ON':
        switchOn(infoWin,100,60,'Green')
    else:
        switchOff(infoWin,100,60)

#Preload switch
    if preloadSet == 'ON':
        switchOn(infoWin,200,60,'Blue')
    else:
        switchOff(infoWin,200,60)

#Discharge delay switch
    if dischargeDelay == 'ON':
        switchOn(infoWin,300,60,'Blue')
    else:
        switchOff(infoWin,300,60)

#Octopus switch
    if octopus == 'ON':
        switchOn(infoWin,400,60,'Green')
    else:
        switchOff(infoWin,400,60)

#Free session switch
    if freeTag == 'ON':
        switchOn(infoWin,500,60,'Green')
    else:
        switchOff(infoWin,500,60)

#Charge auto button
    if chargeAuto == 'ON':
        makeButton(infoWin,100,170,'Light Green')
    else:
        makeButton(infoWin,100,170,'White')

#Discharge auto button
    if dischargeAuto == 'ON':
        makeButton(infoWin,100,300,'Light Green')
    else:
        makeButton(infoWin,100,300,'White')

#Charge block button
    if chargeBlock == 'ON':
        makeButton(infoWin,500,170,'Red')
    else:
        makeButton(infoWin,500,170,'White')

#Charge force button
    if chargeForce == 'ON':
        makeButton(infoWin,430,170,'Blue')
        dischargeBlock = touch(infoWin,360,300,'Red')
        exportForce = untouch(infoWin,360,300)
        dischargeAuto = untouch(infoWin,100,300)
    else:
        makeButton(infoWin,430,170,'White')

#Discharge block button
    if dischargeBlock == 'ON':
        makeButton(infoWin,500,300,'Red')
    else:
        makeButton(infoWin,500,300,'White')

# Discharge force button
    if dischargeForce == 'ON':
        makeButton(infoWin,430,300,'Blue')
        chargeBlock = touch(infoWin,500,170,'Red')
        chargeAuto = untouch(infoWin,100,170)
        chargeForce = untouch(infoWin,430,170)
    else:
        makeButton(infoWin,430,300,'White')

# Export button
    if exportForce == 'ON':
        makeButton(infoWin,360,300,'Blue')
        chargeBlock = touch(infoWin,500,170,'Red')
        chargeAuto = untouch(infoWin,100,170)
        chargeForce = untouch(infoWin,430,170)
    else:
        makeButton(infoWin,360,300,'White')

# Write charge time
    csTime, csHrs, csMins = byteTime(chargeStart)
    ceTime, ceHrs, ceMins = byteTime(chargeEnd)
    chargeTimes = "From " + csTime + " to " + ceTime
    writeTimes(infoWin,230,170,chargeTimes)

# Write discharge time
    dsTime, dsHrs, dsMins = byteTime(dischargeStart)
    deTime, deHrs, deMins = byteTime(dischargeEnd)
    dischargeTimes = "From " + dsTime + " to " + deTime
    writeTimes(infoWin,230,300,dischargeTimes)

# Write charging percentage
    percent = getInvPercent(inverterAddress)
    writePercent(infoWin,340,170,'to ' + percent + '%')
    sendInvPercent(inverterAddress,infoWin,percent)


    try:
        while True:
   # Mouse click on master window
            m = win.checkMouse()
            if m != None:
                infoWin.close()
                return solcast,preloadSet,dischargeDelay,setPreload,octopus,freeTag,fStartHrs, fStartMins, fEndHrs, fEndMins, offset

    # Return pressed
            m = infoWin.checkMouse()
            if m != None:
                if (m.x > 250) and (m.x < 350) and (m.y > 350) and (m.y < 390):
                    infoWin.close()
                    return solcast,preloadSet,dischargeDelay,setPreload,octopus,freeTag,fStartHrs, fStartMins, fEndHrs, fEndMins, offset

     # Solcast switch pressed
                x = 100
                y = 60
                if (m.x > x-38) and (m.x < x+38) and (m.y > y-8) and (m.y < y+8):
                    solcast = toggle(infoWin,x,y,'Green',solcast)

    # Preload switch pressed
                x = 200
                y = 60
                if (m.x > x-38) and (m.x < x+38) and (m.y > y-8) and (m.y < y+8):
                    preloadSet = toggle(infoWin,x,y,'Blue',preloadSet)

    # Discharge delay switch pressed
                x = 300
                y = 60
                if (m.x > x-38) and (m.x < x+38) and (m.y > y-8) and (m.y < y+8):
                    dischargeDelay = toggle(infoWin,x,y,'Blue',dischargeDelay)

    # Octopus switch pressed
                x = 400
                y = 60
                if (m.x > x-38) and (m.x < x+38) and (m.y > y-8) and (m.y < y+8):
                    octopus = toggle(infoWin,x,y,'Green',octopus)
                     
    # Free session switch pressed
                x = 500
                y = 60
                if (m.x > x-38) and (m.x < x+38) and (m.y > y-8) and (m.y < y+8):
                    freeTag = toggle(infoWin,x,y,'Green',freeTag)
                if freeTag == 'ON':
                    fStartHrs, fStartMins, fEndHrs, fEndMins, offset = setFree(fStartHrs, fStartMins, fEndHrs, fEndMins, offset, win, infoWin)
                    

    # Charge auto button pressed
                x = 100
                y = 170
                if (dischargeForce.upper() != 'ON') and (exportForce.upper() != 'ON'):
                    if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                        chargeAuto = touch(infoWin,x,y,'Light Green')
                        oldChargeAuto = chargeAuto
                        chargeBlock = untouch(infoWin,500,170)
                        chargeForce = untouch(infoWin,430,170)
                        chargeStart, chargeEnd, dischargeStart, dischargeEnd = getTimes()
                        setWait(infoWin)
                        sendInvMode(inverterAddress,infoWin,selfMode)
                        sendInvTimes(inverterAddress,infoWin,chargeStart,chargeEnd,dischargeStart,dischargeEnd)
                        unsetWait(infoWin)

    # Charge block button pressed
                x = 500
                y = 170
                if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                    chargeBlock = touch(infoWin,x,y,'Red')
                    chargeAuto = untouch(infoWin,100,170)
                    chargeForce = untouch(infoWin,430,170)
                    saveTimes(chargeStart,chargeEnd,dischargeStart,dischargeEnd)
                    setWait(infoWin)
                    sendInvMode(inverterAddress,infoWin,selfMode)
                    sendInvTimes(inverterAddress,infoWin,0,0,dischargeStart,dischargeEnd)
                    unsetWait(infoWin)

    # Charge force button pressed
                x = 430
                y = 170
                if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                    chargeForce = touch(infoWin,x,y,'Blue')
                    chargeAuto = untouch(infoWin,100,170)
                    chargeBlock = untouch(infoWin,500,170)
                    dischargeForce = untouch(infoWin,430,300)
                    exportForce = untouch(infoWin,360,300)
                    dischargeAuto = untouch(infoWin,100,300)
                    dischargeBlock = touch(infoWin,500,300,'Red')
                    saveTimes(chargeStart,chargeEnd,dischargeStart,dischargeEnd)
                    setWait(infoWin)
                    sendInvMode(inverterAddress,infoWin,manualMode)
                    sendManMode(inverterAddress,infoWin,forceCharge)
                    unsetWait(infoWin)

    # Discharge suto button pressed
                x = 100
                y = 300
                if chargeForce.upper() != 'ON':
                    if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                        dischargeAuto = touch(infoWin,x,y,'Light Green')
                        oldDischargeAuto = dischargeAuto
                        dischargeBlock = untouch(infoWin,500,300)
                        dischargeForce = untouch(infoWin,430,300)
                        exportForce = untouch(infoWin,360,300)
                        chargeStart, chargeEnd, dischargeStart, dischargeEnd = getTimes()
                        setWait(infoWin)
                        sendInvMode(inverterAddress,infoWin,selfMode)
                        sendInvTimes(inverterAddress,infoWin,chargeStart,chargeEnd,dischargeStart,dischargeEnd)
                        unsetWait(infoWin)

    # Discharge block button pressed
                x = 500
                y = 300
                if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                    dischargeBlock = touch(infoWin,x,y,'Red')
                    dischargeAuto = untouch(infoWin,100,300)
                    dischargeForce = untouch(infoWin,430,300)
                    exportForce = untouch(infoWin,360,300)
                    saveTimes(chargeStart,chargeEnd,dischargeStart,dischargeEnd)
                    setWait(infoWin)
                    sendInvMode(inverterAddress,infoWin,selfMode)
                    sendInvTimes(inverterAddress,infoWin,chargeStart,chargeEnd,0,0)
                    unsetWait(infoWin)

    # Discharge force button pressed
                x = 430
                y = 300
                if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                    dischargeForce = touch(infoWin,x,y,'Blue')
                    dischargeAuto = untouch(infoWin,100,300)
                    dischargeBlock = untouch(infoWin,500,300)
                    exportForce = untouch(infoWin,360,300)
                    chargeForce = untouch(infoWin,430,170)
                    chargeAuto = untouch(infoWin,100,170)
                    chargeBlock = touch(infoWin,500,170,'Red')
                    saveTimes(chargeStart,chargeEnd,dischargeStart,dischargeEnd)
                    setWait(infoWin)
                    sendInvMode(inverterAddress,infoWin,selfMode)
                    sendInvTimes(inverterAddress,infoWin,chargeStart,chargeEnd,0,15127)
                    unsetWait(infoWin)

    # Export button pressed
                x = 360
                y = 300
                if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                    exportForce = touch(infoWin,x,y,'Light Green')
                    dischargeAuto = untouch(infoWin,100,300)
                    dischargeBlock = untouch(infoWin,500,300)
                    dischargeForce = untouch(infoWin,430,300)
                    chargeForce = untouch(infoWin,430,170)
                    chargeAuto = untouch(infoWin,100,170)
                    chargeBlock = touch(infoWin,500,170,'Red')
                    saveTimes(chargeStart,chargeEnd,dischargeStart,dischargeEnd)
                    setWait(infoWin)
                    sendInvMode(inverterAddress,infoWin,manualMode)
                    sendManMode(inverterAddress,infoWin,forceDischarge)
                    unsetWait(infoWin)

    # Charge time pressed
                if (m.x > 150) and (m.x < 310) and (m.y > 158) and (m.y < 182):
                    if chargeAuto.upper() == 'ON':
                        stime,shrs,smins = byteTime(chargeStart)
                        etime,ehrs,emins = byteTime(chargeEnd)
                        shrs,smins,ehrs,emins = SetTimes.setTimes(shrs,smins,ehrs,emins,'Charge from', win,infoWin)
                        csTime = str(shrs) + ":" + str(smins + 100)[1:3]
                        ceTime = str(ehrs) + ":" + str(emins + 100)[1:3]
                        chargeTimes = "From " + csTime + " to " + ceTime
                        chargeStart = timeByte(shrs,smins)
                        chargeEnd = timeByte(ehrs,emins)
                        writeTimes(infoWin,230,170,chargeTimes)
                        setWait(infoWin)
                        sendInvTimes(inverterAddress,infoWin,chargeStart,chargeEnd,dischargeStart,dischargeEnd)
                        unsetWait(infoWin)

    # Charge percentage pressed
                if (m.x > 320) and (m.x < 410) and (m.y > 158) and (m.y < 182):
                    if chargeAuto.upper() == 'ON':
                        percent = SetTimes.setPercent(int(percent), win, infoWin)
                        writePercent(infoWin,340,170,'to ' + str(percent) + '%')
                        setWait(infoWin)
                        sendInvPercent(inverterAddress,infoWin,percent)
                        unsetWait(infoWin)


    # Discharge time pressed
                if (m.x > 150) and (m.x < 310) and (m.y > 288) and (m.y < 312):
                    if dischargeAuto.upper() == 'ON':
                        stime,shrs,smins = byteTime(dischargeStart)
                        etime,ehrs,emins = byteTime(dischargeEnd)
                        shrs,smins,ehrs,emins = SetTimes.setTimes(shrs,smins,ehrs,emins,'Discharge from', win, infoWin)
                        dsTime = str(shrs) + ":" + str(smins + 100)[1:3]
                        deTime = str(ehrs) + ":" + str(emins + 100)[1:3]
                        dischargeTimes = "From " + dsTime + " to " + deTime
                        dischargeStart = timeByte(shrs,smins)
                        dischargeEnd = timeByte(ehrs,emins)
                        writeTimes(infoWin,230,300,dischargeTimes)
                        setWait(infoWin)
                        sendInvTimes(inverterAddress,infoWin,chargeStart,chargeEnd,dischargeStart,dischargeEnd)
                        unsetWait(infoWin)

    # reset auto block on charge
                x = 100
                y = 300
                if chargeForce.upper() != 'ON':
                    if (dischargeForce.upper() != 'ON') and (exportForce.upper() != 'ON') and (oldChargeAuto != chargeAuto):
                        if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                            chargeAuto = touch(infoWin,100,170,'Light Green')
                            chargeBlock = untouch(infoWin,500,170)
                            chargeForce = untouch(infoWin,430,170)

    # reset auto block on discharge
                x = 100
                y = 170
                if (dischargeForce.upper() != 'ON') and (exportForce.upper() != 'ON'):
                    if (chargeForce.upper() != 'ON') and (oldDischargeAuto != dischargeAuto):
                        if (m.x > x-30) and (m.x < x+30) and (m.y > y-30) and (m.y < y+30):
                            dischargeAuto = touch(infoWin,100,300,'Light Green')
                            dischargeBlock = untouch(infoWin,500,300)
                            dischargeForce = untouch(infoWin,430,300)
                            exportForce = untouch(infoWin,360,300)

            time.sleep(0.1)
    except:
        try:
            infoWin.close()
            return solcast,preloadSet,dischargeDelay,setPreload,octopus,freeTag,fStartHrs, fStartMins, fEndHrs, fEndMins, offset
        except:
            return solcast,preloadSet,dischargeDelay,setPreload,octopus,freeTag,fStartHrs, fStartMins, fEndHrs, fEndMins, offset


def switchOff(infoWin,x,y):
    switch = Circle(Point(x-20,y),12)
    switch.setFill('Light Gray')
    switch.setOutline('Light Gray')
    switch.draw(infoWin)

    slide = Rectangle(Point(x-20,y-10),Point(x+20,y+10))
    slide.setFill('White')
    slide.setOutline('White')
    slide.draw(infoWin)

    switch = Circle(Point(x+20,y),10)
    switch.setFill('White')
    switch.setOutline('White')
    switch.draw(infoWin)

    switch = Circle(Point(x-20,y),12)
    switch.setFill('Gray')
    switch.setOutline('Black')
    switch.draw(infoWin)

def switchOn(infoWin,x,y,colour):

    switch = Circle(Point(x-20,y),12)
    switch.setFill('Light Gray')
    switch.setOutline('Light Gray')
    switch.draw(infoWin)

    slide = Rectangle(Point(x-20,y-10),Point(x+20,y+10))
    slide.setFill(colour)
    slide.setOutline(colour)

    slide.draw(infoWin)

    switch = Circle(Point(x-20,y),10)
    switch.setFill(colour)

    switch.setOutline(colour)
    switch.draw(infoWin)

    switch = Circle(Point(x+20,y),12)
    switch.setFill('Gray')
    switch.setOutline('Black')
    switch.draw(infoWin)

def toggle(infoWin,x,y,colour,state):
    if state.upper() == 'OFF':
        switchOn(infoWin,x,y,colour)
        return 'ON'
    else:
        switchOff(infoWin,x,y)
        return 'OFF'

def makeButton(infoWin,x,y,colour):
    button = Rectangle(Point(x - 30,y - 30),Point(x+30,y+30))
    button.setFill('White')
    button.draw(infoWin)

    shading = Polygon(Point(x-30,y-30),Point(x-30,y+30),Point(x,y))
    shading.setFill('Light Gray')
    shading.draw(infoWin)

    shading = Polygon(Point(x+30,y-30),Point(x+30,y+30),Point(x,y))
    shading.setFill('Dark Gray')

    shading.draw(infoWin)

    shading = Polygon(Point(x+30,y+30),Point(x-30,y+30),Point(x,y))
    shading.setFill('Gray')
    shading.draw(infoWin)

    button = Circle(Point(x,y),26)
    button.setFill(colour)
    button.setOutline('Black')
    button.draw(infoWin)

def touch(infoWin,x,y,colour):
    button = Circle(Point(x,y),26)
    button.setFill(colour)
    button.setOutline('Black')
    button.draw(infoWin)
    return 'ON'

def untouch(infoWin,x,y):
    button = Circle(Point(x,y),26)
    button.setFill('White')
    button.setOutline('Black')
    button.draw(infoWin)
    return 'OFF'

def saveTimes(chargeStart,chargeEnd,dischargeStart,dischargeEnd):
    data = {"chargeStart": chargeStart,"chargeEnd": chargeEnd,"dischargeStart": dischargeStart,"dischargeEnd": dischargeEnd}
    dataJson = json.dumps(data)
    f = open("times.json", "w")
    f.write(dataJson)
    f.close()

def getTimes():
    if os.path.exists("times.json"):
        f = open("times.json", "r")
        dataJson = f.read()
        data = json.loads(dataJson)
        chargeStart = data["chargeStart"]
        chargeEnd = data["chargeEnd"]
        dischargeStart = data["dischargeStart"]
        dischargeEnd = data["dischargeEnd"]
        return chargeStart,chargeEnd,dischargeStart,dischargeEnd
    else:
        return Settings.startCheapRate + (Settings.crMins * 256), Settings.endCheapRate + (Settings.prMins * 256), Settings.noDelay * 60, 15127

def byteTime(byte):
    mins = int(int(byte)/256)
    hrs = int(byte) - (mins * 256)
    time = str(hrs) + ":" + (str(mins+100)[1:3])
    return time,hrs,mins

def timeByte(hrs,mins):
    byte = mins*256 + hrs
    return byte

def writeTimes(infoWin,x,y,times):
    rect = Rectangle(Point(x-80,y-12), Point(x+80,y+12))
    rect.setFill("Light Gray")
    rect.setOutline('Light Gray')
    rect.draw(infoWin)
    text = Text(Point(x,y),times)
    text._reconfig("font",("Arial",14,"bold"))
    text.draw(infoWin)

def writePercent(infoWin,x,y,percent):
    rect = Rectangle(Point(x-32,y-12), Point(x+32,y+12))
    rect.setFill("Light Gray")
    rect.setOutline('Light Gray')
    rect.draw(infoWin)
    time.sleep(0.04)
    text = Text(Point(x,y),percent)
    text._reconfig("font",("Arial",14,"bold"))
    text.draw(infoWin)

def getInvTimes(inverterAddress):
    data = 'optType=ReadSetData&pwd='+ Settings.inverterPassword
    x = requests.post(inverterAddress, data=data)
    x = (x.text)
    y = x[1:]
    array = re.split(",",y)
    chargeStart = array[dchReg-3]
    chargeEnd = array[dchReg-2]
    dischargeStart = array[dchReg-1]
    dischargeEnd = array[dchReg]
    return chargeStart,chargeEnd,dischargeStart,dischargeEnd

def getInvMode(inverterAddress):
    data = 'optType=ReadSetData&pwd='+ Settings.inverterPassword
    x = requests.post(inverterAddress, data=data)
    x = (x.text)
    y = x[1:]
    array = re.split(",",y)
    mode = array[modeReg-1]
    return mode

def getManMode(inverterAddress):
    data = 'optType=ReadSetData&pwd='+ Settings.inverterPassword
    x = requests.post(inverterAddress, data=data)
    x = (x.text)
    y = x[1:]
    array = re.split(",",y)
    manMode = array[manReg-1]
    return manMode

def getInvPercent(inverterAddress):
    data = 'optType=ReadSetData&pwd='+ Settings.inverterPassword
    x = requests.post(inverterAddress, data=data)
    x = (x.text)
    y = x[1:]
    array = re.split(",",y)
    percent = array[chgReg-1]
    return percent

def sendInvTimes(inverterAddress,infoWin,chargeStart,chargeEnd,dischargeStart,dischargeEnd):
    set3.set(inverterAddress, Settings.inverterPassword, dchReg-2, chargeStart)
    set3.set(inverterAddress, Settings.inverterPassword, dchReg-1, chargeEnd)
    set3.set(inverterAddress, Settings.inverterPassword, dchReg, dischargeStart)
    set3.set(inverterAddress, Settings.inverterPassword, dchReg+1, dischargeEnd)

def sendInvPercent(inverterAddress,infoWin,percent):
    set3.set(inverterAddress, Settings.inverterPassword, chgReg, percent)

def sendInvMode(inverterAddress,infoWin,mode):
    set3.set(inverterAddress, Settings.inverterPassword, modeReg, mode)

def sendManMode(inverterAddress,infoWin,manMode):
    set3.set(inverterAddress, Settings.inverterPassword, manReg, manMode)

def setWait(infoWin):
    rect = Rectangle(Point(250,350), Point(350,390))
    rect.setFill("Red")
    rect.setOutline('Black')
    rect.draw(infoWin)

    text = Text(Point(300,370),'Wait')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(infoWin)

def unsetWait(infoWin):
    rect = Rectangle(Point(250,350), Point(350,390))
    rect.setFill("White")
    rect.setOutline('Black')
    rect.draw(infoWin)

    text = Text(Point(300,370),'Return')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(infoWin)

def setFree(fStartHrs, fStartMins, fEndHrs, fEndMins, offset, win, infoWin):
    fStartHrs, fStartMins, fEndHrs, fEndMins = SetTimes.setTimes(fStartHrs, fStartMins, fEndHrs, fEndMins, "Free Period", win, infoWin)
    offset = offset - (fEndHrs - fStartHrs) * 20
    return fStartHrs, fStartMins, fEndHrs, fEndMins, offset
        
