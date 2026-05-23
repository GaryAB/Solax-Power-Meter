###Using the script as an embedded system

The Meter7.8 script when used on a Raspberry Pi can be used either from the Graphical User Interface (GUI) as a script under Thony, or it can be used as an embedded system which will run automatically every time that the Raspberry Pi is rebooted.

In order to do this, some changes are required to the operating system.

First, change the ‘run’ line in **Settings.py** to “AUTO”

>run = “MANUAL”                    #Change to “AUTO” if running script automatically (see manual)

This modifies the script slightly, including adding a twenty-second delay at startup to allow the GUI on the Raspberry Pi to fully boot up and connect to WiFi.

Next, open the command line window and type the following:

>sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

This will open the nano text editor with the autostart file
Move your cursor to the bottom of the file and type:

>@/usr/bin/python /home/yourname/folder/Meter7.8.py

Where **yourname** is the name of your home folder, **Meter7.8.py** is the current version of the script and **folder** is the folder where the script is placed.

Close the file with **Ctrl-X** and reboot your Raspberry Pi.

The script should now start about 20 seconds after the Pi has rebooted. You will note that the window now has an ‘Escape’ symbol at the bottom right, pressing this will enable you to minimise the script and get back to the standard Pi GUI.

The script contains a built-in watchdog timer. If any process takes longer than 30 seconds, the Raspberry Pi will reboot. This should not affect the operation of the script, but if, for some reason, the script does not restart after the reboot, delete the temporary files; all those ending in **.json** then reboot the Pi again. Note that this will lose your previous data, and the script will start from scratch.

Any errors which have occurred during the running of the script will be added to the file **errlog.txt**, which can be viewed in any text editor.   

For further resilience, I recommend rebooting the Raspberry Pi at regular intervals. This can be done automatically. I reset the Pi at 8.50 every morning. To achieve this, do the following:

In the Pi’s command line, type the following:

>crontab -e

If you have not done this before, you will be given the option of which text editor to use. The default is nano.
At the bottom of the page, type the following:

>50 8 * * * sudo reboot

Close the text editor and reboot.

The time can be changed to your convenience. Do not however, be tempted to reboot overnight, as the script may assume that the backup file is out of date and ignore it when starting. 
Reboot either before the start or after the end of your off-peak electricity period. 
I also recommend not rebooting on the hour as the script carries out some functions on the hour, which may be missed due to the reboot.

Note that when running as an embedded system, the backup and log files are created in your root directory rather than in the same directory as the script.

