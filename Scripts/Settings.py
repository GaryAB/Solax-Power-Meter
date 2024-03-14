#Settings

#This file can be edited with any text editor, but please take care and make sure that text strings are enclosed in quotation marks 
# and that your text editor does not try and correct any spellings.
 
scale = 5                         #scale of meter in kW
tokenID = '12345678912345678912'  #API Token from Solax cloud website
inverterPassword = 'SXXXXXXXXX'   #password to access inverter - found from SolaX Cloud website
startCheapRate = 0                #Start of cheap rate electricity in hours (LOCAL or UTC, See below)
crMins = 0                        #Set to minutes if cheap rate starts at a time other than on the hour
endCheapRate = 7                  #Start of full rate electricity in hours (LOCAL or UTC, See below)
prMins = 0                        #Set to minutes if peak rate starts at a time other than on the hour
timeZone = "LOCAL"                #Set to "UTC" if rate changes do not change with daylight saving
solcast = "OFF"                   #Set to "ON" if using Solcast to forecast overnight preload (see Manual)
log = "NO"                        #set to "YES" to log data to a CSV file

# The following settings are for Meter7.7 only 

inverterAddress = '5.8.8.8'       #address of inverter - use '5.8.8.8' if logged into inverter's access point
                                  #if the address is not static,  enter 'dchp'
                                  #Set DCHP range of your router on the lines below
From = '192.168.1.1'              #Start of address range for DCHP allocation
To = '192.168.1.254'              #End of address range for DCHP allocation
preloadSet = "MANUAL"             #Set to "AUTO" to allow app to automatically set the overnight charging limit.
offset = 0                        #percentage offset added to recommended preload
dischargeDelay = "MANUAL"         #set to "AUTO" if you wish to use the discharge delay facility
noDelay = 8                       #set earliest time for battery discharge in hours. e.g. 8 means 8am, 13 means 1pm.
