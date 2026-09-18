### Instructions for using Meter7.9.py

7.9 is the latest version of Power Meter, which has several improvements over previous versions of the script.

First, it displays the energy exported as well as that used from the grid. The Pylon symbol above the export figure indicates the direction of power to and from the grid.
It has a Boost function which will provide a timed discharge from the batteries, either to feed the house or to export to the grid. It also has an improved algorithm to measure the energy imported and exported from the inverter, which overcomes a previous problem resulting from the inverter's software. The script now monitors the inverter every 15 seconds rather than every 30 seconds as in previous versions, and there is an EV mode which attempts to prevent your car emptying the contents of your house battery when it is being charged.

The Meter7.9 script, when used on a Raspberry Pi, can be run either from the Graphical User Interface (GUI) as a script under Thony or as an embedded system that runs automatically every time the Raspberry Pi is rebooted. That requires some editing of the operating system on the Raspberry Pi, so read **Using the script as an embedded system**.

Meter 7.9.py has its settings in a separate file **Settings.py**.
This file can be edited with any text editor, but please take care and make sure that text strings are enclosed in quotation marks and that your text editor does not try and correct any spellings.

For details on editing this file, read **Settings.md** in the **Manual** folder.

Meter7.9.py displays PV power, battery power, excess power to the grid and the current battery state of charge.
It also displays the energy used from the grid during peak (daytime), off-peak (nighttime) periods and energy exported during the day.

With the Solcast module activated, it displays an estimated overnight preload of the battery to make the best use of both PV power and battery power.
Meter7.9.py also has the ability to set the battery preload automatically, and on days with little solar yield can delay the use of batteries until the early evening. For this purpose, Meter 7.9 also learns your average usage of electricity on each day of the week. 

Pressing or clicking on the cogwheel symbol at the top left of the screen opens a control panel which enables you to change the mode of the inverter or change the set charge and discharge times. For further details, read **Using the Control Panel**. 

Pressing on the timer symbol at the bottom left of the screen opens the Boost dialogue, read **Using the Boost facility** to understand the Boost function.

The script can create a log file called **powerlog.csv**, which can be entered into a spreadsheet program for further processing.
The values logged are Solar yield, Battery use, Grid power used during daytime, Grid power used during nighttime off-peak, and Exported energy to the grid over the previous 24 hours. Note that for this purpose, the 24 hours start at the beginning of the off-peak period.
These values are not logged by the SolaX cloud, but are calculated by the script; therefore, for accurate values, the script must run continuously.
Each 24 hours starts at the beginning of the off-peak period or midnight if no off-peak period is set.
Note that when you first run the script, the first day's log may not be recorded or may be incomplete.

The script creates four temporary files on your drive. **power.json** stores the details from the last access to the inverter and allows the script to resume after a restart. **daymeans.json** stores average daily power usage to be used by the Solcast module, and **Set_bak.json** is a backup file of your current settings. **Times.json** is a backup of your battery charge and discharge times. 

If updating from a previous version of the script earlier than Meter 7.7, you must delete the old **power.json** file before running **Meter7.9.py** as the format has changed.

As well as **Settings.py**, Meter7.9 requires several external modules, all of which must be in the same directory as the main script.
It also requires a modified version of graphics.py by John Zelle, called **graphics3.py** which is included in the repository. All these are contained in the **scripts** directory in the Github repository.

To install, I recommend that you click on the green **Code** block in Github and download the Zip file, then unzip it on the Raspberry Pi. Extract the **scripts** folder to your home directory then rename it as you see fit.

Meter 7.9 can also be used on systems other than the Raspberry Pi, but the Auto mode uses Linux system commands which may create errors on other operating systems.
