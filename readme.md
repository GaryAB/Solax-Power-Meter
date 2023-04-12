A Python script to display a user-friendly front end to a Solax X1 Hybrid G4 inverter.

![](/Pictures/Display.jpg)

Written to run on a Raspberry Pi with a four-inch Hyperpixel display, but can be run on other implementations of Python. For full functionality, it needs to run continuously.

Displays PV power, battery power, excess power to grid and the current battery state of charge.
Also displays power used from the grid during peak (daytime) and off-peak (nighttime) periods.

![](Pictures/Grid.jpg)

With the Solcast module activated it displays an estimated overnight precharge of the battery to make the best use of both PV power and battery power.

![](/Pictures/Preload.jpg)

Two scripts are included, Meter6.2.py which takes its data from the Solax Cloud (and may work with other inverters) and Meter7.2.py which takes its data directly from the inverter.
Meter7.2.py updates every thirty seconds, whereas the Solax Cloud is only updated once every five minutes.

Full instructions in the **manual** folder
 
