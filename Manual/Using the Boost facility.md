### Using the Boost facility

**Boost** is a new function in Meter7.9.py

It is used to allow you to turn on battery power for a fixed period, when the battery is otherwise not discharging.

For example, you may have the battery discharge time set to 4 pm in order to use the batteries during the peak time in the evening.
If you want to use something that is going to take electricity earlier in the day, say a tumble dryer, without taking power from the grid, you can use the Boost function to allow a time limited discharge.

To use Boost, click or press on the **Timer** icon at the bottom left of the screen. This will open the Boost dialogue box.

![](/Pictures/Boost.png)

If you press the first button, you will get an immediate* boost for 30 minutes.
If you press the second button you will get a boost lasting for one hour.
Pressing the third button will allow you to set a Boost to operate any time that you wish within the next 24 hours. 
Set the time using the nudge panel that appears, then press **Return**.

A limit can be set on how much to allow the batteries to discharge. To set this, simply touch the relevant point on the bar at the bottom of the window. (Python unfortunately does not allow the point to be changed by sliding the finger/mouse). 

The **Permanent** switch at the bottom right of the page can be turned on if you want the boost to repeat each day at the same time. 

Note that you can only set the limit higher than the current battery state of charge if the **Permanent** switch is turned on.

Do not forget to press **Return** to close the Boost dialogue and allow the app to continue.

*Although I say immediate, sending data to the inverter may take up to 30 seconds, but it may take up to a minute before the change is reflected on the display.

If you want to end a Boost before it is finished, open the Boost dialogue and press the 'illuminated' button so that it returns to white, then press **Return**.

If you want to extend a Boost period, open the Boost dialogue and either press the illuminated button twice, or press an alternative button then press **Return**.

The second row is identical to the first, except that any power not used by the house will be exported to the grid.

As the boost functions are totally controlled by the script, the script must be running for the boost instructions to be sent to the inverter.

Note that the discharge limit only applies during the boost period and does not limit the discharge of the batteries after the boost session has finished.
