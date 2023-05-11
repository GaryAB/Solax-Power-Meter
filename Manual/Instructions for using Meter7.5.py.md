###Instructions for using Meter7.5.py

To use Meter7.5 you will, first, need to set the scale for the meter display. The scale value needs to be set, in kW, to a value more than the maximum power you need to display.
For example, the default value is 5, ideal for a 4kWp solar array and a 3.68kW inverter. If your solar array is 7kW peak and your inverter is 5kW then set scale to 8.

>scale = 5 #scale of meter in kW

Meter7.5 can be used in two ways. You can either log into the inverter's WiFi access point directly or you can contact the inverter via your house WiFi.
The SSID of the inverter starts WiFI_S followed by nine digits.
In this case you should leave the IP number in the script to the default 5.8.8.8

To connect via your house WiFi, you need to know whether your inverter has beens set with a static IP number or whether it is relying on the DCHP function of your router.
If you know that the IP address is static, then enter that address into the Inverter Address line in the script.
If not, then enter **dchp** between the quotation marks. When you run the script it will search your WiFi to find the inverter. If your router should change the inverter's IP address, the script will search again.
You also need to enter the DCHP range of your router on the two following lines. The default values will be correct for most domestic routers as supplied by your ISP. 

>inverterAddress = 'dchp'          #address of inverter - use '5.8.8.8' if logged into inverter's access point
>                                  
>From = '192.168.1.1'              #Start of address range for DCHP allocation
>
>To = '192.168.1.254'              #End of address range for DCHP allocation
>

Note that if the DCHP range is large, the search process may take several minutes.

Next you need to enter the password for your inverter which is the registration number of the inverter's Pocket Wifi. This is the second half of the SSID after the underscore.
It can also be found on the Solax Cloud website.  
Go to the Inverter page and copy the Registration number which starts with the letter S. Paste it into the password line in the script. 

>inverterPassword = 'SXXXXXXXXX'   #Password to access inverter - get from Solax Cloud website 

If you have peak and off-peak electricity tariffs, put the time of the start of each into the next two lines (hours only). The default settings are 0 and 7 relating to 'Economy 7' in the UK.

>startCheapRate = 0                #Start of cheap rate electricty in hours (UTC)
>
>endCheapRate = 7                  #Start of full rate electricity in hours (UTC)

Note that because the clock on your electricity meter is not automatically reset during the summer to cope with daylight saving time, these have to be entered in UTC (GMT) **not** local time. 
The peak and off-peak usage is not available from the inverter, instead it is counted by the script itself. In order for these to be accurate the script has to run continuously. If the script is stopped for any length of time, these values will no longer be correct.
These figures will remain blank until some usage has been measured.

If you want to use the Solcast module, change the word 'OFF' to 'ON' and read the instructions on setting up Solcast.
   
Note that Solcast will not work if you are logged directly into the inverter's access point as you will not have access to the internet.

Meter7.5 also has the ability to set the charge limit on the inverter automatically.
If you want to use this function change the word 'MANUAL' to 'AUTO'. Meter7.5 will then automatically set the preload value and tell you what value it has set.

The Offset setting allows you to adjust the value set by the script. The default is zero, but I find that a value of 10 to 15 is effective as it allows for some use of cheap power before the sun rises as well as allowing some tolerance on the predicted solar yield for the next day. 

>solcast = "ON"                    #Set to "ON" if using Solcast to forecast overnight preload (see notes)
>
>preloadSet = "AUTO"               #Set to "AUTO" to allow app to automatically set the overnight charging limit.
>
>offset = 0                        #percentage offset added to recommended preload

Note that for this to work the inverteer must be in **Self Use** mode with **Charge from grid** enabled. This and the charge and discharge period need to be set from the SolaX app or SolaX Cloud as normal.

Meter7.5 requires three external modules, **Solcast4.py**, **scan.py** and **set.py**.

The script also creates two temporary files on your drive. **power.json** stores the details from the last access to the inverter and allows the script to resume after a restart.
**daymeans.json** stores average daily power usage to be used by the Solcast module.
