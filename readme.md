###A Python script to display a user-friendly front end to a Solax X1 Hybrid G4 inverter.

Written to run on a Raspberry Pi with a four-inch Hyperpixel display, but can be run on other implementations of Python. For full functionality, it needs to run continuously.

Displays PV power, battery power, excess power to grid and the current battery state of charge. Also displays energy used from the grid during peak (daytime) and off-peak (nighttime) periods and the amount of energy exported.

![](/Pictures/Display.png)

With the Solcast module activated it displays an estimated overnight preload of the battery to make the best use of both PV power and battery power.

![](/Pictures/Preload.png)

Two scripts are included, Meter6.9.py which takes its data from the Solax Cloud (and may work with other inverters) and Meter7.9.py which takes its data directly from the inverter.

Meter 7.9 has several new features. As well as displaying exported energy, it has a control panel to modify the programme settings and directly control the solar panel inverter. Both scripts use a new algorithm to measure the power taken from the grid, to overcome a shortcoming of the SolaX inverter software.

![](/Pictures/Control.png)

It has a 'Boost' mode which allows a timed discharge of the house battery when it otherwise would not be used, and it can detect and adjust the inverter for Octopus savings sessions.

Meter7.9.py also has the ability to automatically set the overnight preload of the battery and adjust the use of the battery the next day to avoid the battery becoming completely discharged before the evening peak. It also has an EV mode to prevent car charging completely exhausting the house batteries.

![](/Pictures/Set_to.png)

Both scripts can be enabled as embedded systems on a Raspberry Pi, starting automatically on boot up. 

Full instructions are in the **manual** folder. For convenience, there is also a PDF version of the manual whch can be printed or read without being logged into Github.
 

