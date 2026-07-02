### Instructions for using Meter7.8/py with the new SolaX Pocket Dongle v4.0

With the new version of the pocket WiFi dongle, Solax have made some changes which have defeated the use of Power Meter via your house WiFi.

It is however possible to use the full functions of Meter 7.8 on a Raspberry Pi, but it requires a bit more work.

First, you will need a cable connection from your internet router to the ethernet socket of your Raspberry Pi.

If your router is WiFi only, then this system will not work.

Having cable connected your Raaspberry Pi to your router, you need to open the router's management page and make sure that the IP number for the SolaX dongle: 192.168.10.10 is outside the range that the router can 'see'. This will prevent any accidental IP clashes. The common IP for household routers:192.168.1.1 and the subnet mask of 255.255.255.0 are ideal for this. If your router has an IP number in the range 192.168.10.1 to 192.168.10.254 then you will have to change it. 

In the settings file for Meter 7.8 set the inverter address to 192.168.10.10

>inverterAddress = '192.168.10.10'          #address of inverter - use '5.8.8.8' if logged into inverter's access point
>                                  #or 192.168.10.10 if you have the later WiFi module.

Next, on your Rapsberry Pi, open the terminal and type

>sudo nano /ext/wpa_supplicant/wpa_supplicant.conf

This should open a page looking like this:

![](/Pictures/Supplicant_old.png)

Edit the page to the following. Note that you will need to use the arrow keys on your keyboard to mave around as the mouse does not work on this page.

![](/Pictures/Supplicant_new.png)

where the letters after **WiFi_** are the registration number of your WiFi dongle. Do not delete or modify the first three lines.

Go to your inverter and press the control button once on your WiFi dongle. This will start the dongle's access point (AP). This will only remain active for a few monutes before turning off again. While the AP is running reboot your Raspberry Pi and the Pi should connect to the dongle's AP.
This will be indicated by the symbol at the top of the Pi's screen, ringed in red in the image below.

![](/Pictures/WiFi_indicator.png)

Once the connection is made the AP should remain active. Note that only one device at a time can access the AP, so local control on your phone app will not work while the Pi is connected.

Now run Meter7.8.py. I recommend running it from Thony the first time as that will enable you to see any problems. If all is well the script should show the current status of the inverter. 

I recommend, while Meter 7.8 is running, to open the built-in browser and make sure that you can still access the internet. If you can, then the Solcast and Octopus functions of Meter 7.8 should work.

If you wish to set up Meter 7.8 to run as an embedded system, you can now do so, but remember to press the control button on the SolaX dongle to restart the AP before rebooting the Pi.

All the above applies to the Raspberry Pi, but a similar method will work with other systems including a PC, but you will have to use the appropriate commands for that system to access the inverter and internet simultaneously.


 
