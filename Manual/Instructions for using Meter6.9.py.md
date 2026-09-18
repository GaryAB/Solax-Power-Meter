### Instructions for using Meter6.9.py

Meter6.9.py has its settings in a separate file **Settings.py**.
This file can be edited with any text editor, but please take care and make sure that text strings are enclosed in quotation marks and that your text editor does not try to correct any spellings.

For details on editing this file, read **Settings.md** in the **Manual** folder.

Meter6.9.py displays PV power, battery power, excess power to the grid and the current battery state of charge.
It also displays the energy used from the grid during peak (daytime) and off-peak (nighttime) periods plus any exports back to the grid.

The pylon symbol shows whether power is currently going to or from the grid. A black pylon means that no power is flowing. The pylon will turn blue if power is being received from the grid and red if it is being exported.

With the Solcast module activated, the script will display an estimated overnight preload of the battery to make the best use of both PV power and battery power.

The script can create a log file called **powerlog.csv**, which can be entered into a spreadsheet program for further processing.
The values logged are Solar yield, Battery use, Grid power used during daytime, Grid power used during nighttime off-peak, and Exported energy to the grid over the previous 24 hours.
These values are not logged by the SolaX cloud, but are calculated by the script, therefore for accurate values, the script must run continuously.
Each 24 hours starts at the beginning of the off-peak period or midnight if no off-peak period is set.
Note that when you first run the script, the first day's log may not be recorded or may be incomplete.

For users of Octopus Energy the script can also detect Octopus Savings Sessions, although unlike Meter 7.9 it cannot set the inverter, that will have to be done manually via either the SolaX Cloud website or the SolaX app.

The script creates two temporary files on your drive. **power.json** stores the details from the last access to the inverter and allows the script to resume quickly after a restart. 
**daymeans.json** stores average daily power usage for the Solcast module.

The format of these files is now identical to those for Meter 7.9. so you can move seamlessly between the two scripts.
 
If updating from a version of the script prior to Meter 6.7, you must delete the old **power.json** file before running **Meter6.9.py** as the format has changed.

Meter6.9.py requires four external modules, **Solcast4.py**, **Week2.py**, **Octopus5.py** and **powerlog.py**, which must be in the same directory as the main script along with the graphics files.
It also requires a special version of graphics.py by John Zelle, called **graphics3.py** which is included in the repository. 

