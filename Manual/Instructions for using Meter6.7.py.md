###Instructions for using Meter6.7.py

Unlike previous versions of this application, Meter6.7.py has the settings in a separate file **Settings.py** rather than editing the main script.
This file can be edited with any text editor, but please take care and make sure that text strings are enclosed in quotation marks and that your text editor does not try and correct any spellings.

For details on editing this file read **Settings.md** in the **Manual** folder.

Meter6.7.py displays PV power, battery power, excess power to grid and the current battery state of charge.
Also displays power used from the grid during peak (daytime) and off-peak (nighttime) periods.

With the Solcast module activated it displays an estimated overnight preload of the battery to make the best use of both PV power and battery power.

The script can create a log file called **powerlog.csv** which can be entered into a spreadsheet program for further processing.
The values logged are, Solar yield, Battery use, Grid power used during daytime, Grid power used during nighttime off-peak, Exported energy to the grid over the previous 24 hours. Note that for this purpose the 24 hours starts at the beginning of the off peak period.
These values are not logged by the SolaX cloud, but are calculated by the script, therefore for accurate values the script must run continuously.
Each 24 hours starts at the beginning of the off-peak period or midnight if no off-peak is set.
Note that when you first run the script, the first day's log may not be recorded or my be incomplete.
Also due to the discontinuous nature of the monitoring of the inverter by the SolaX Cloud, the values for Solar Yield and Battery Use should be considerd as estimates.

The script creates two temporary files on your drive. **power.json** stores the details from the last access to the inverter and allows the script to resume quickly after a restart.
**daymeans.json** stores average daily power usage for the Solcast module.
 
If updating from a previous version of the script, you must delete the old **power.json** file before running **Meter6.7.py** as the format has changed.

Meter6.7.py requires three external modules, **Solcast4.py**, **Week2.py**, and **powerlog.py** which must be in the same directory as the main script.
It also requires **graphics.py** by John Zelle which is included in the repositry. 

