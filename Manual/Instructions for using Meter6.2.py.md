Instructions for using Meter6.2.py

To use Meter6.2 you will, first, need both the password and the token ID from the Solax Cloud.

Assuming that your inverter has been linked to the Cloud by your installer, first log into the Solax Cloud website at [https://www.solaxcloud.com](https://www.solaxcloud.com).

![](/Pictures/SolaxRegNo.jpg)

Go to the Inverter page and copy the Registration number which starts with the letter S. This is also your password, so paste it into the password line in the script. 
>inverterPassword = 'SXXXXXXXXX'  #Password to access inverter - get from Solax Cloud website

![](/Pictures/SolaxAPI.jpg)

Next, go to the API page (under Service) where you can create and copy your Token ID. Paste this into the tokenID line in the script. 
Remember to keep both token and password within the quotation marks.
>tokenID = '12345678912345678912' #API Token from Solax cloud website

If you have peak and off-peak electricity tariffs, put the time of the start of each into the next two lines (hours only). The default settings are 0 and 7 relating to 'Economy 7' in the UK.

>startCheapRate = 0  #Start of cheap rate electricty in hours (UTC)
>
>endCheapRate = 7  #Start of full rate electricity in hours (UTC)

Note that because the clock on your electricity meter is not reset during the summer to cope with daylight saving time, these have to be entered in UTC (GMT) **not** local time. 

The peak and off-peak usage is not available from the Cloud, instead it is counted by the script itself. In order for these to be accurate the script has to run continuously. If the script is stopped for any length of time, these values will no longer be correct.
These figures will remain blank until some usage been measured.

If you want to use the Solcast module, change the word 'OFF' to 'ON' and read the instructions on setting up Solcast.   

The script creates two temporary files on your drive. **power.json** stores the details from the last access to the inverter and allows the script to resume after a restart.
**daymeans.json** stores average daily power usage for the Solcast module.
