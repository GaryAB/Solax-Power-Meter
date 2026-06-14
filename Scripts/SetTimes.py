from graphics import *
import time

# Dummy data
shrs = 0
smins = 30
ehrs = 4
smins = 30

def setTimes(shrs,smins,ehrs,emins,cText,win,infoWin):

    timesWin = GraphWin("Set Times",400,350)

    rect = Rectangle(Point(0,0), Point(400,350))
    rect.setFill('light gray')
    rect.draw(timesWin)

    rect = Rectangle(Point(150,290), Point(250,330))
    rect.setFill("White")
    rect.setOutline('Black')
    rect.draw(timesWin)

    text = Text(Point(200,310),'Return')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(timesWin)

    text = Text(Point(200,25),cText)
    text._reconfig("font",("Arial",14,"normal"))
    text.draw(timesWin)

    text = Text(Point(200,155),'until')
    text._reconfig("font",("Arial",14,"normal"))
    text.draw(timesWin)


    drawScrollBox(timesWin,80,50,str(shrs) + ':' + str(smins+100)[1:3], win, infoWin)
    drawScrollBox(timesWin,80,180,str(ehrs) + ':' + str(emins+100)[1:3], win, infoWin)

    shrs,smins,ehrs,emins = doScrollBox(timesWin,shrs,smins,ehrs,emins, win, infoWin)

    return shrs,smins,ehrs,emins

def drawScrollBox(timesWin,x,y,timeString, win, infoWin):

    rect = Rectangle(Point(x,y), Point(x+240,y+70))
    rect.setFill('White')
    rect.draw(timesWin)

    rect = Rectangle(Point(x,y), Point(x+30,y+70))
    rect.setFill('White')
    rect.draw(timesWin)

    rect = Rectangle(Point(x+210,y), Point(x+240,y+70))
    rect.setFill('White')
    rect.draw(timesWin)

    upArrow = Polygon(Point(x+15,y+2),Point(x+2,y+30),Point(x+28,y+30))
    upArrow.setFill('Black')
    upArrow.draw(timesWin)

    dnArrow = Polygon(Point(x+15,y+68),Point(x+2,y+40),Point(x+28,y+40))
    dnArrow.setFill('Black')
    dnArrow.draw(timesWin)

    upArrow = Polygon(Point(x+225,y+2),Point(x+212,y+30),Point(x+238,y+30))
    upArrow.setFill('Black')
    upArrow.draw(timesWin)

    dnArrow = Polygon(Point(x+225,y+68),Point(x+212,y+40),Point(x+238,y+40))
    dnArrow.setFill('Black')
    dnArrow.draw(timesWin)

    text = Text(Point(x+120,y+35),timeString)
    text._reconfig("font",("Arial",40,"normal"))
    text.draw(timesWin)

def doScrollBox(timesWin,shrs,smins,ehrs,emins,win,infoWin):
    while True:
   # Mouse click on master window
        m = win.checkMouse()
        if m != None:
            timesWin.close()
            infoWin.close()
            return shrs,smins,ehrs,emins

   # Mouse click on control panel
        m = infoWin.checkMouse()
        if m != None:
            timesWin.close()
            return shrs,smins,ehrs,emins

        m = timesWin.checkMouse()
        if m != None:
            if (m.x >150) and (m.x < 250) and (m.y > 290) and (m.y < 330):
                timesWin.close()
                return shrs,smins,ehrs,emins

            x = 80
            y = 50
            if (m.x > x) and (m.x < x+30) and (m.y > y) and (m.y < y+30):
                shrs = shrs+1
                if shrs == 24:
                    shrs = 0

            if (m.x > x) and (m.x < x+30) and (m.y > y+40) and (m.y < y+70):
                shrs = shrs-1
                if shrs == -1:
                    shrs = 23

            if (m.x > x+210) and (m.x < x+240) and (m.y > y) and (m.y < y+30):
                smins = (10*int(smins/10))+10
                if smins == 60:
                    smins = 0
                    shrs = shrs+1
                    if shrs == 24:
                        shrs = 0

            if (m.x > x+210) and (m.x < x+240) and (m.y > y+40) and (m.y < y+70):
                smins = smins-1
                if smins == -1:
                    smins = 59
                    shrs = shrs-1
                    if shrs == -1:
                        shrs = 23

            x = 80
            y = 180
            if (m.x > x) and (m.x < x+30) and (m.y > y) and (m.y < y+30):
                ehrs = ehrs+1
                if ehrs == 24:
                    ehrs = 0

            if (m.x > x) and (m.x < x+30) and (m.y > y+40) and (m.y < y+70):
                ehrs = ehrs-1
                if ehrs == -1:
                    ehrs = 23

            if (m.x > x+210) and (m.x < x+240) and (m.y > y) and (m.y < y+30):
                emins = (10*int(emins/10))+10
                if emins == 60:
                    emins = 0
                    ehrs = ehrs+1
                    if ehrs == 24:
                        ehrs = 0

            if (m.x > x+210) and (m.x < x+240) and (m.y > y+40) and (m.y < y+70):
                emins = emins-1
                if emins == -1:
                    emins = 59
                    ehrs = ehrs-1
                    if ehrs == -1:
                        ehrs = 23

            x = 80
            y = 50
            rect = Rectangle(Point(x+30,y), Point(x+210,y+70))
            rect.setFill('White')
            rect.draw(timesWin)

            text = Text(Point(x+120,y+35),str(shrs) + ':' + str(smins+100)[1:3])
            text._reconfig("font",("Arial",40,"normal"))
            text.draw(timesWin)

            x = 80
            y = 180
            rect = Rectangle(Point(x+30,y), Point(x+210,y+70))
            rect.setFill('White')
            rect.draw(timesWin)

            text = Text(Point(x+120,y+35),str(ehrs) + ':' + str(emins+100)[1:3])
            text._reconfig("font",("Arial",40,"normal"))
            text.draw(timesWin)

            time.sleep(0.1)

def setPercent(percent, win, infoWin):

    timesWin = GraphWin("Settings",400,350)

    rect = Rectangle(Point(0,0), Point(400,350))
    rect.setFill('light gray')
    rect.draw(timesWin)

    rect = Rectangle(Point(150,290), Point(250,330))
    rect.setFill("White")
    rect.setOutline('Black')
    rect.draw(timesWin)

    text = Text(Point(200,310),'Return')
    text._reconfig("font",("Arial",12,"normal"))
    text.draw(timesWin)

    text = Text(Point(200,95),'Charge to')
    text._reconfig("font",("Arial",14,"normal"))
    text.draw(timesWin)

    drawScrollBox(timesWin,80,120,str(percent) + '%', win, infoWin)

    percent = doScrollPercent(timesWin,percent, win, infoWin)

    return percent

def doScrollPercent(timesWin,percent, win, infoWin):
    while True:
   # Mouse click on master window
        m = win.checkMouse()
        if m != None:
            timesWin.close()
            infoWin.close()
            return percent

   # Mouse click on control panel
        m = infoWin.checkMouse()
        if m != None:
            timesWin.close()
            return percent

        m = timesWin.checkMouse()
        if m != None:
            if (m.x >150) and (m.x < 250) and (m.y > 290) and (m.y < 330):
                timesWin.close()
                return percent

            x = 80
            y = 120
            if (m.x > x) and (m.x < x+30) and (m.y > y) and (m.y < y+30):
                if percent <= 85:
                    percent = percent + 10

            if (m.x > x) and (m.x < x+30) and (m.y > y+40) and (m.y < y+70):
                if percent >= 20:
                    percent = percent - 10

            if (m.x > x+210) and (m.x < x+240) and (m.y > y) and (m.y < y+30):
                if percent < 95:
                    percent = percent + 1

            if (m.x > x+210) and (m.x < x+240) and (m.y > y+40) and (m.y < y+70):
                if percent > 10:
                    percent = percent - 1

            rect = Rectangle(Point(x+30,y), Point(x+210,y+70))
            rect.setFill('White')
            rect.draw(timesWin)

            text = Text(Point(x+120,y+35),str(percent) + '%')
            text._reconfig("font",("Arial",40,"normal"))
            text.draw(timesWin)


            time.sleep(0.1)
