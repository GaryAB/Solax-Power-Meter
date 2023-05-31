##Error Messages

The Meter6.6.py and Meter7.6.py scripts have the ability to display error messages when a problem occurs.
Here are the relevant messages and what they mean:

>Unable to contact cloud

Meter6.6.py has lost contact with the SolaX Cloud

>Unable to contact inverter

Meter7.6.py has lost contact with the inverter

Both these errors may only be temporary. The script will wait for 5 minutes then try again.
If the message becomes permanent, check your WiFi and in the case of Meter6.5, your internet connection.

>Too many failures contacting cloud/inverter

The cloud or inverter are not returning valid data. The script will try 5 times to get valid data and if it fails this message will appear.
Check that your inverter password and in the case of Meter6.5, your API token, have been entered correctly.

>Unable to contact Solcast

The script cannot access the Solcast website. Try the website in a browser to see if it is live: https://toolkit.solcast.com.au.
Remember that Meter7.6 cannot access the internet when connected directly to the SolaX inverter's access point.

>Data invalid from Solcast

Solcast is not returning valid data. Check the Solcast Key and Resource ID from the Solcast website. Set up Solcast on the website if you have not already done so.

The following errors only apply to Meter7.5:

>Inverter not found

Meter7.6 in DCHP mode has not been able to find the inverter on your local WiFi. This error may only be temporary. The script will wait for 5 minutes then try again.
If the message becomes permanent, check that you are connected to the right WiFi network. Check that the router's DCHP range has been entered correctly.

Note: I have noticed that the inverter goes off-line occasionally, perhaps when it is accessing the Cloud. In this case, this message may appear but it will usually reconnect at the next attempt.

>Wrong type of inverter

The script is not connected to a single-phase SolaX X1-Hybrid-G4 inverter. In this case use Meter6.6.py instead.

>Unable to set preload to...

For some reason Meter7.6 has been unable to automatically set the preload value. Use the SolaX Cloud or the SolaX app to set the preload manually.

>Charge from grid disabled

Meter7.6 cannot set the preload as **Charge from grid** is disabled at the inverter. 
Use the SolaX Cloud or the SolaX app to enable **Charge from grid** in **Self use** in the inverter settings. Make sure that **Work mode** is set to **Self use**.  
 
>Inverter fault

The inverter is returning that it is in a fault condition. Visit the SolaX Cloud website and look for the red dot in the header. This is the warning log which will give you more details of the fault.

