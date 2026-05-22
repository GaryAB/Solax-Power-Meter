###Instructions for use of Octopus functions

Power Meter v.7.10 can now automatically detect an Octopus Saving Session and control the inverter durng the session. 

Power Meter detects when Octopus' bid to save power hae been accepted by reading the National Grid API. This does not guarantee that you will be offered a saving session, but one is at least taking place in your area..

As the bids are regionalised, it is important that Power Meter knows which region you live in. The respective regions are:  

North Scotland

South and Central Scotland

North East England

North West England

Yorkshire

East Midlands

West Midlands

London

East England

South East England

South West England

Southern England

North Wales Merseyside and Cheshire

South Wales

If you do not know which region you are in, the map is currently available at:https://www.neso.energy/data-portal/gis-boundaries-gb-dno-license-areas/gb_dno_licence_areas_20240503

The appropriate region must be entered into **Settings.py**. Take particular note of the spelling and capitalisation above as the text has to be indentical to that in the API.

>octopus = "YES"                   #set to "YES" to automatically reset battery discharge time if an Octopus Saving Session is happening

>region = "East England"           #set to your National Grid region - see Octopus instructions

>ssExport = "YES"                  #set to "YES" to export during saving sessions

When the saving session is detected, the discharge start time is adjusted to the start of the savings session. If **ssExport** is set to "YES" then the batteries will export during the saving session to increase the posible return. When the saving session is complete, the system will be returned to its normal automatic mode. Note that if you are normally setting the discharge start time manually, you will have to do so again after the saving session is complete. As well as the settings in Settings.py, the Octopus function can be turned on and off in the Control Panel.

**Octopus Free Sessions**

At present these cannot be automatically detected, but if you are offered one, you can turn the **Free Session** function on in the Control Panel. These sessions will normally be offered the day before, so when you receive one, turn the Control Panel option on and you will then be presented with a scroll panel to set the start and end times. Press return and then close the control panel.

The overnight preload, if set automatically, will be reduced to allow some space in the batteries ready for the free session. When the free session starts, the batteries will be switched to charge from the grid until either the session ends or the batteries reach 95% full. At this point the session will end and the status returned to normal.

Remember that the Octopus functions will only operate if you are accessing the inverter via your local network and your Raspberry Pi still has access to the internet.

