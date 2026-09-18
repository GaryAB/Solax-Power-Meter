### Instructions for use of Octopus functions

Power Meter v.7.9 can now automatically detect an Octopus Saving Session and control the inverter during the session. 

Power Meter detects when Octopus' bid to save power has been accepted by reading the National Grid (NESO) API. This does not guarantee that you will be offered a saving session, but one is at least taking place in your area..

As the bids are regionalised, Power Meter must know which region you live in. The regions have recently been reorganised and now have numbers rather than names.

If you wish to know which region you are in, view the map below:

![](/Pictures/DFS_Map.jpg)

The appropriate region must be entered into **Settings.py**. Enter it as a number without quotation marks. 

>octopus = "YES"                   #set to "YES" to automatically reset battery discharge time if an Octopus Saving Session is happening

>region = 10                       #set to your National Grid region - see Octopus instructions

>ssExport = "YES"                  #set to "YES" to export during saving sessions

When the saving session is detected, the discharge start time is adjusted to the start of the saving session. If **ssExport** is set to "YES", then the batteries will export during the saving session to increase the possible return. When the saving session is complete, the system will be returned to its normal automatic mode. Note that if you are normally setting the discharge start time manually, you will have to do so again after the saving session is complete. As well as the settings in **Settings.py**, the Octopus functions can be turned on and off in the Control Panel. 

**Octopus Free Sessions**

At present, these cannot be automatically detected, but if you are offered one, you can turn the **Free Session** function on in the Control Panel. These sessions will normally be offered the day before, so when you receive one, turn the Control Panel option on and you will then be presented with a scroll panel to set the start and end times. Press return and then close the control panel.

The overnight preload, if set automatically, will be reduced to allow some space in the batteries ready for the free session. When the free session starts, the batteries will be switched to charge from the grid until either the session ends or the batteries reach 95% full. At this point the session will end and the status will return to normal.

The latest version of the NESO API, also allows for free sessions. So far none have occurred, but if one is offered, it will be set up exactly the same as the Octopus Free Sessions mentioned above.

Remember that the Octopus functions will only operate if you are connected to both your inverter and to the wider internet.

As the Octopus functions are totally controlled by the script, the script must be running during the session, otherwise the instructions will not be received by the inverter.

