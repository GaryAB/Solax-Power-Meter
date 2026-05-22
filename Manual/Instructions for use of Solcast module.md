###Instructions for use of Solcast module

The Solcast module **Solcast4.py** downloads the next day's estimated solar yield from [toolkit.solcast.com.au]{toolkit.solcast.com.au} and uses it to calculate how much energy to add to the home batteries on an overnight off-peak rate to make the best use of the batteries and solar panels.

The first requirement is to go to the Solcast website and sign up. You then need to enter your precise location and the details of your solar array.

Once you have done that, you need to select your site which will take you to the page showing a graph of estimated solar yield.

In *Site Summary* you will see a Resource ID. Click on this and it will be copied to your clipboard. Paste into Settings.py in the Resource ID line remembering to put it within the quotation marks.

![](/Pictures/SolcastResource.jpg)

>resourceID = 'XXXX-XXXX-XXXX-XXXX' # obtain from Solcast website

In the download section near the bottom of the page, select *Find your API key here*. Click *Copy Key* then paste it into the solcastKey line in Settings.py

![](/Pictures/SolcastAPII.jpg)

>solcastKey = 'ABCDEFGHIJKLMONPQRSTUVWXYZ123456' # obtain from Solcast website

Finally enter the capacity of your home batteries in kWh.

>capacity = 11.6 # Capacity of battery in kWh

In the settings file, set the solcast line to ON

>solcast = "ON"  #Set to 'ON' if using Solcast to forecast overnight preload (see notes)

Each evening at 9pm local time, the script will obtain the latest forecast from Solcast and calculate the recommended preload for the batteries for that night.

![](/Pictures/Preload.jpg)

The script will continue to display the result until 1am allowing plenty of time to change the setting on the inverter. 

If **preloadSet** is set to 'AUTO' then scripts Meter7.7.py and later will automatically set the preload for the batteries.

>preloadSet = "AUTO"               #Set to "AUTO" to allow app to automatically set the overnight charging limit.
>offset = 30                       #percentage offset added to recommended preload

A percentage offset can be added to the preload setting in order to account for local differences to the prediction, e.g. partial shading by a tree.

**dischargeDelay** if set to AUTO will allow the script to set a delay of up to eight hours to the use of the batteries on days of low sun, in order that power is retained for use in the peak hours in the evening, rather than using all of the battery power first thing in the morning. 

>dischargeDelay = "MANUAL"         #set to "AUTO" if you wish to use the discharge delay facility
>noDelay = 7                       #set earliest time for battery discharge in hours. e.g. 8 means 8am, 13 means 1pm.

**noDelay** sets the earliest time that the batteries will discharge on days of good sunlight. 

The calsulation also uses an estimate of your likely use of power during the next day. The estimate is based on previous use for that day of the week. 
It will probably take a few weeks to generate a reasonably accurate estimate. The calculation is based on filling the battery by 3pm local time. 

I take no responsibilty for the accuracy or otherwise of Solcast's predictions.
