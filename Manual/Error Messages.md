### Error Messages

The Meter6.9.py and Meter7.9.py scripts have the ability to display error messages when a problem occurs.
Here are the relevant messages and what they mean:

>Unable to contact cloud

Meter6.9.py has lost contact with the SolaX Cloud

>Unable to contact inverter

Meter7.9.py has lost contact with the inverter

Both these errors may only be temporary. The script will wait for 5 minutes then try again.
If the message becomes permanent, check your WiFi and in the case of Meter6.9, your internet connection.

>Too many failures contacting cloud/inverter

The cloud or the inverter is not returning valid data. The script will try 5 times to get valid data, and if it fails, this message will appear.
Check that your inverter password and, in the case of Meter6.9, your API token, have been entered correctly.

>Unable to contact Solcast

The script cannot access the Solcast website. Try the website in a browser to see if it is live: [https://toolkit.solcast.com.au/](https://toolkit.solcast.com.au/)
Remember that Meter 7.9 cannot access the internet when only connected directly to the SolaX inverter's access point.

>Data invalid from Solcast

Solcast is not returning valid data. Check the Solcast Key and Resource ID from the Solcast website. Set up Solcast on the website if you have not already done so.

The following errors only apply to Meter7.7 onwards:

>Inverter not found

Meter7.9 in DHCP mode has not been able to find the inverter on your local WiFi. This error may only be temporary. The script will wait for 5 minutes, then try again.
If the message becomes permanent, check that you are connected to the right WiFi network. Check that the router's DHCP range has been entered correctly.

Note: I have noticed that the inverter goes offline occasionally, perhaps when it is accessing the Cloud. In this case, this message may appear, but it will reconnect at the next attempt.

>Wrong type of inverter

The script is not connected to a single-phase SolaX X1-Hybrid-G4 inverter. In this case, use Meter6.9.py instead.

>Unable to set preload to...

For some reason, Meter7.9 has been unable to automatically set the preload value. Use the SolaX Cloud or the SolaX app to set the preload manually.

>Discharge time not set

For some reason, Meter7.9 has been unable to set the battery discharge start time. Use the SolaX cloud or the SolaX app to check the current setting and change it if necessary.

>Charge from grid disabled

Meter7.9 cannot set the preload as **Charge from grid** is disabled at the inverter. 
Use the SolaX Cloud or the SolaX app to enable **Charge from grid** in **Self use** mode on the inverter. Make sure that **Work mode** is set to **Self use**.  
 
>Inverter fault

The inverter is returning that it is in a fault condition. Visit the SolaX Cloud website and go to the Alarms page (Bell icon at left). This is the warning log which will give you more details of the fault.

The following messages only applies to Meter6.9.py and Meter7.9.py

>Corrupt backup file

The backup file is corrupt. As the back up file **Power.json** is written so often, this can occasionally happen due to no fault of the script. In this event the script will not display power from grid or exported power until valid results are available and a new back up file is created. That day's log will also not be written. If this error persists, it is time to replace your SD card as the card is becoming unreliable.

>Using default settings

This error will occur if the settings back up file **Set_bak.json** is corrupted or is from an earlier version of the script. In this event the script will use the settings from the **Settings.py** file. Open the Control Panel to check your settings. This will create a new file.
