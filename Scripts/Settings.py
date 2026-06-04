#Settings 
scale = 5                           #scale of meter in kW
tokenID = '12345678912345678912'    #API Token from Solax cloud website
inverterPassword = 'SXXXXXXXXX'     #password to access inverter - found from SolaX Cloud website
startCheapRate = 0                  #Start of cheap rate electricty in hours (Local or UTC, see below)
crMins = 0                          #Set to minutes if cheap rate starts at a time other than on the hour
endCheapRate = 7                    #Start of full rate electricity in hours (Local or UTC)
prMins = 0                          #Set to minutes if peak rate starts at a time other than on the hour
timeZone = "LOCAL"                  #Set to "UTC" if rate changes do not change with daylight saving
solcast = "OFF"                     #Set to 'ON' if using Solcast to forecast overnight preload (see notes)
log = "YES"                         #set to "YES" to log data to a CSV file

# The following settings are for Meter7.7+ only 

inverterAddress = 'dchp'          #address of inverter - use '5.8.8.8' if logged into inverter's access point
                                  #or 192.168.10.10 if you have the later WiFI module.
                                  #if logging into your house WiFi and the address is not static,  enter 'dchp'
                                  #Set DCHP range of your router on the lines below
From = '192.168.1.1'              #Start of address range for DCHP allocation
To = '192.168.1.254'              #End of address range for DCHP allocation
preloadSet = "MANUAL"             #Set to "AUTO" to allow app to automatically set the overnight charging limit.
offset = 0                        #percentage offset added to recommended preload
dischargeDelay = "MANUAL"         #set to "AUTO" if you wish to use the discharge delay facility
noDelay = 7                       #set earliest time for battery discharge in hours. e.g. 8 means 8am, 13 means 1pm.
run = "MANUAL"                    #Change to "AUTO" if running script automatically (see manual)

# The following settings are for Meter 7.8 onwards only

octopus = "NO"                   #set to "YES" to automatically reset battery discharge time if an Octopus Saving Session is happening
region = 10                      #set to your National Grid region - see Octopus instructions
ssExport = "NO"                  #set to "YES" to export during saving sessions

# The following settings are for the Solcast addon

solcastKey = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef' # obtain from Solcast website
resourceID = 'abcd-1234-efgh-5678'              # obtain from Solcast website
capacity = 11.6                                 # Capacity of battery in kWh
efficiency = 80                                 # Battery efficiency input to output in percent
                                                # default is 80

# After making changes to this file, delete the file set_bak.json
# which may either be in the current folder or in your root folder.
