Instructions for using Meter7.2.py

Meter7.2 can be used in two ways. You can either log into the inverter's WiFi access point directly or you can connect to the inverter via your house WiFi.
The SSID of the inverter starts WIFI_S followed by nine digits.
In this case you should leave the IP number in the script to the default 5.8.8.8

If you intend to connect to the inverter via your home's WiFi you first need to find out the IP number allocated to the inverter and put that IP number into the inverter address in the script.
Note that this IP address could change unless you have set up a static IP for the inverter.

> inverterAddress = '192.168.1.112'  #address of inverter - use '5.8.8.8' if logged into inverter's access point 

Next you need to enter the password for your inverter which is the registration number of the inverter's Pocket Wifi. This is the second half of the SSID after the underscore.
It can also be found on the Solax Cloud website by going to the Inverter page and copying the Registration number which starts with the letter S. Paste it into the password line in the script. 

>inverterPassword = 'SXXXXXXXXX'  #Password to access inverter - get from Solax Cloud website 

If you have peak and off-peak electricity tariffs, put the time of the start of each into the next two lines (hours only). The default settings are 0 and 7 relating to 'Economy 7' in the UK.

>startCheapRate = 0  #Start of cheap rate electricty in hours (UTC)
>
>endCheapRate = 7  #Start of full rate electricity in hours (UTC)

Note that because the clock on your meter is not reset during the summer to cope with daylight saving time, these have to be entered in UTC (GMT) **not** local time. 
The peak and off-peak usage is not available from the inverter, instead it is counted by the script itself. In order for these to be accurate the script has to run continuously. If the script is stopped for any length of time, these values will no longer be correct.
These figures will remain blank until some usage been measured.

If you want to use the Solcast module, change the word 'OFF' to 'ON' and read the instructions on setting up Solcast.   

Note that Solcast will not work if you are logged directly into the inverter's access point as you will have no access to the internet.

The script creates two temporary files on your drive. **power.json** stores the details from the last access to the inverter and allows the script to resume after a restart.
**daymeans.json** stores average daily power usage to be used by the Solcast module.
