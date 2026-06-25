###Instructions for **Settings.py**

Before you can use Meter7.8.py, you will first have to edit the settings for your solar installation.

This file can be edited with any text editor, but please take care and make sure that text strings are enclosed in quotation marks and that your text editor does not try to correct any spellings.

You will first need to set the scale for the meter display. The scale value needs to be set, in kW, to a value more than the maximum power you need to display.
For example, the default value is 5, ideal for a 4kWp solar array and a 3.68kW inverter. If your solar array is 7kW peak and your inverter is 5kW, then set **scale** to 8.

>scale = 5 #scale of meter in kW

Next, you will need to know both the password and the token ID from the Solax Cloud.

Assuming that your inverter has been linked to the Cloud by your installer, first log in to the Solax Cloud website at [https://www.solaxcloud.com](https://www.solaxcloud.com).

![](/Pictures/SolaxRegNo.jpg)

Go to the Inverter page and copy the Registration number, which starts with the letter S. This is also your password, so paste it into the password line in the script. 
>inverterPassword = 'SXXXXXXXXX'  #Password to access inverter - get from Solax Cloud website

![](/Pictures/SolaxAPI.jpg)

Next, go to the API page (under Service) where you can create and copy your Token ID. Paste this into the tokenID line in the script. 
Remember to keep both the token and the password within the quotation marks.

>tokenID = '12345678912345678912' #API Token from Solax cloud website

Note that the tokenId is not essential for Meter7.7.py onwards, as they do not use the SolaX cloud API.

If you have peak and off-peak electricity tariffs, put the time of the start of each into the next four lines. The default settings relate to 'Economy 7' in the UK. 
If your energy supplier has a rate change which occurs other than on the hour, you can set the number of minutes after the hour.

>startCheapRate = 0                #Start of cheap rate electricity in hours (LOCAL or UTC, See below)

>crMins = 0                        #Set to minutes if cheap rate starts at a time other than on the hour

>endCheapRate = 7                  #Start of full rate electricity in hours (LOCAL or UTC, See below)

>prMins = 0                        #Set to minutes if peak rate starts at a time other than on the hour

If you do not receive off-peak power overnight, set all these values to zero.

Note that some older electricity meters are not automatically reset during the summer to cope with daylight saving time. If this is the case, you should enter the times in UTC (GMT) **not** local time and set the timeZone setting to "UTC" rather than "LOCAL".

>timeZone = "LOCAL"                #Set to "UTC" if rate changes do not change with daylight saving

The peak and off-peak usage is not available from the inverter; instead, it is counted by the script itself. In order for these to be accurate, the script has to run continuously. If the script is stopped for any length of time, these values may no longer be correct.
These figures will remain blank until some usage has been measured.

If you want to use the Solcast module, change the word 'OFF' to 'ON' and read the instructions on setting up Solcast. Even if you are not using it, the Solcast module needs to be present in your directory.

Power Meter 6.7 and 7.7 onwards now also have the ability to create a log of energy used. Enter "YES" in the line 'log ='

>log = "YES"                       #set to "YES" to log data to a text file

**The next settings apply only to Meter7.8.py**

Meter7.8 can be used in two ways. You can either log into the inverter's WiFi access point (AP) directly, or you can contact the inverter via your house WiFi.
The SSID of the inverter starts with WiFi_S followed by nine digits.
In this case, you should set the IP number in the script to '5.8.8.8'. If you have the newer Wifi module on the inverter with 10-second updates, the IP number needs to be 192.168.10.10. 

**Note** I have recently been told that later versions of the software on SolaX inverters no longer allow access to the API via your house WiFi. In this case, you **must** operate Meter 7.8 connected to the inverter's AP. This will mean that you will lose the ability to use the Solcast and Octopus modules, as you will not have access to the internet. 

To connect via your house WiFi, you need to know whether your inverter has been set with a static IP number or whether it is allocated by your router.
If you know that the IP address is static, then enter that address into the Inverter Address line in the script.
If not, then enter **dchp** between the quotation marks. When you run the script, it will search your WiFi to find the inverter. If your router should change the inverter's IP address, the script will search again.
You also need to enter the DCHP range of your router on the two following lines. The default values will be correct for most domestic routers as supplied by your ISP. 

>inverterAddress = 'dchp'          #address of inverter - use '5.8.8.8' if logged into inverter's access point

>#or 192.168.10.10 if you have the later WiFI module.

>#if logging into your house WiFi and the address is not static,  enter 'dchp'

>#Set the DHCP range of your router on the lines below

>From = '192.168.1.1'              #Start of address range for DCHP allocation

>To = '192.168.1.254'              #End of address range for DCHP allocation

Note that if the DCHP range is large, the search process may take several minutes.

In addition, Meter 7.8 has a facility which delays the start of the battery discharge phase on days of very poor solar yield so that there is still power available from the batteries in the early evening, when the grid is under the greatest load.
On certain tariffs, this will also save you money (e.g. Octopus Flux).
This function delays the discharge start time for up to eight hours, depending on the estimated daytime usage. 
To enable this function, set dischargeDelay to "AUTO".

>dischargeDelay = "AUTO"           #set to "AUTO" if you wish to use the discharge delay facility

Set noDelay to the earliest time that you want the batteries to start discharging. The default is 7 am. This is the setting you would normally use in the SolaX app.

>noDelay = 7                       #set earliest time for battery discharge in hours. e.g. 8 means 8 am, 13 means 1 pm.

The run setting should be set to 'AUTO' if you are using the script as an embedded system; otherwise, leave it as 'MANUAL'. 

The next settings are for the use of the Octopus functions for those who use Octopus as their electricity supplier. For details of these, read the instructions for the Octopus module.
 
The final settings are for the use of the Solcast module. Read the relevant instructions to set these.

Finally, save the edited file to the same folder as the main script, keeping the name **Settings.py**

