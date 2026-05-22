###Instructions for using Meter7.8.py

The Meter7.8 script when used on a Raspberry Pi can be used either from the Graphical User Interface (GUI) as a script under Thony or it can be used as an embedded system which will run automatically every time that the Raspberry Pi is rebooted. That requires some editing of the operating system on the Raspberry Pi, so read **Using the script as an embedded system**.

Meter 7.8.py has its the settings in a separate file **Settings.py**.
This file can be edited with any text editor, but please take care and make sure that text strings are enclosed in quotation marks and that your text editor does not try and correct any spellings.

For details on editing this file read **Settings.md** in the **Manual** folder.

Meter7.8.py displays PV power, battery power, excess power to grid and the current battery state of charge.
Also displays power used from the grid during peak (daytime) and off-peak (nighttime) periods.

With the Solcast module activated it displays an estimated overnight preload of the battery to make the best use of both PV power and battery power.
Meter7.8.py also has the ability to set the battery preload automatically, and on days with little solar yield can delay the use of batteries until the early evening. For this purpose, Meter 7.8 also learns your average useage of electricity on each day of the week. 

Pressing or clicking on the cogwheel symbol at the top left of the screen opens a control panel which enables you to change the mode of the inverter or change the set charge and discharge times. For further details read **Using the Control Panel**.

The script can create a log file called **powerlog.csv** which can be entered into a spreadsheet program for further processing.
The values logged are, Solar yield, Battery use, Grid power used during daytime, Grid power used during nighttime off-peak, Exported energy to the grid over the previous 24 hours. Note that for this purpose the 24 hours starts at the beginning of the off-peak period.
These values are not logged by the SolaX cloud, but are calculated by the script, therefore for accurate values the script must run continuously.
Each 24 hours starts at the beginning of the off-peak period or midnight if no off-peak is set.
Note that when you first run the script, the first day's log may not be recorded or my be incomplete.

The script also creates three temporary files on your drive. **power.json** stores the details from the last access to the inverter and allows the script to resume after a restart. **daymeans.json** stores average daily power usage to be used by the Solcast module, **Set_bak.json** is a back-up file of your current settings. 

If updating from a previous version of the script, you must delete the old **power.json** file before running **Meter7.8.py** as the format has changed.

As well as **Settings.py** Meter7.8 requires several external modules, **Solcast4.py**, **Week2.py**, **scan.py**, **set3.py**, **powerlog.py**, **Freefind2.py**, **Info3.py**, **Octopus5.py**, **SetTimes.py**, **Cog.gif** and **Exit.gif** all of which must be in the same directory as the main script.
It also requires **graphics.py** by John Zelle which is included in the repositry. 

 

+
