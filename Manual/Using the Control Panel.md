### Using the control panel

At the top left of the meter display, there is a cog wheel symbol. Pressing and holding the screen at that point will bring up the control panel.

![](/Pictures/Control.jpg)

The control panel consists of one row of switches at the top and two rows of buttons. The row of switches at the top control features of the application, and the two lower rows control the inverter directly.

The first switch at the top turns on and off the Solcast function, which uses a prediction of the next day’s solar yield to decide how much to preload the battery overnight and how soon to start using the battery to feed the house (read Solcast instructions). 
When the switch is on (to the right and Green) the script will download the Solcast prediction for tomorrow’s solar yield each evening at 9 pm. 
The next two switches control whether the Solcast module should directly control the overnight precharge and the delay before the battery is used the next day.
If **Set Preload** is turned off (left – White), then the app will simply display the recommended preload but not change any settings.
If **Discharge Delay** is on (Blue), the app will also set the time that the battery will begin to be used the next day. 
The two remaining switches are for people who are receiving their grid power from Octopus Electricity. Read the Octopus instructions for further information. 
To toggle a switch, simply touch it with your mouse pointer or finger if using a touch screen.

The top row of buttons controls the charging of the battery from the power grid. 
Normally, the **Auto** button will be pressed (Green), allowing the inverter to switch automatically to charge at the times shown. Touching these times will open a panel with ‘nudge‘ buttons to allow you to change the charge times. 

![](/Pictures/Nudge.jpg)

Tapping on the up and down arrows will set the times. The up-arrow on the right moves the time forward by ten seconds. The down-arrow moves backwards by one second, so any time can be set fairly easily. The left-hand buttons adjust by a complete hour. Press **Return** to return to the Control Panel. 
Touching the charge percentage will open a similar ‘nudge’ panel to allow you to change the percentage overnight precharge.

When making any changes, the **Return** button will turn Red and say **Wait** whilst the instructions are sent to the inverter. This may take up to 30 seconds. 
Once it returns to White press **Return** to close the Control Panel.

Pressing the **Force** button (illuminated in Blue) will force the batteries to charge from the Grid until they either reach 100% charge or you press the **Auto** button again.

Pressing the **Block** button (illuminated in Red) will prevent the batteries from charging from the grid until you press either the **Auto** or **Force** buttons.

The batteries will always charge from solar power, whichever button is pressed.

The bottom row controls the battery discharge.
You can adjust the discharge times in a similar way to the charge times.

Pressing **Block** will prevent the batteries from discharging

Pressing **Force** will force the batteries to discharge to the house.

Pressing **Export** will force the batteries to discharge, but any excess power not required by the house will be sent to the grid.

Do not forget to press **Return** to close the Control Panel after you have used it as that will allow the script to continue.

Settings made in the Control Panel are recorded in the file **Set_bak.json** but changing settings in the panel does not edit the **Settings.py** file.
