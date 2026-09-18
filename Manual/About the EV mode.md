### EV Mode

EV mode came about because a lot of people complain on social media that charging their car causes their house batteries to discharge.

There are ways around this by moving CT clamps on your solar power system, but that is not always possible, so I decided that there may be a way to solve it within the script.

EV mode relies on the fact that most things that take a high load do not do so for very long; ovens and heaters have thermostats, kettles are only on for a short time, so that most high loads will switch off very quickly if only for a moment. Car charging however is a large load which is sustained, and therefore different. 
That can be detected and Meter 7.9 attempts to distinguish between the the car charger and other household loads.

When car charging is detected, the battery discharge will be turned off until the charging has obviously ceased.

In settings you can set a power threshold and a delay before the car charging is detected. 
The correct setting will differ with your charging set up, but with a 7 kW charger, a good setting might be:

>EVmode = "YES"
>carThreshold = 7000
>carDelay = 10

where the script turns off the battery discharge if there is a sustained load of over 7 kW for longer than ten minutes. 
The delay should mean that you only lose slightly more than 1 kWh from your house battery rather than flattening it completely.

Alternatively, if you are using a plug-in 'granny' charger you might set:

>EVmode = "YES"
>carThreshold = 2000
>carDelay = 20

where a sustained load of over 2 kW for more than 20 minutes will switch off the battery discharge.
A larger load, such as a 5 kW oven, should not trigger the EV mode due to the thermostat periodically switching off the oven.

In practice this will be down to experimentation and what works best in your situation.

Bear in mind that some other items, particularly tumble dryers, may also cause the EV function to trigger.
In this event you can effectively cancel EV mode by using the Boost function.

Either way, the purpose is to retain the maximum charge in your house battery until the evening peak.

EV mode only applies in daytime when power is at full price, EV mode is suppressed during the night when electricity is cheap.
EV mode will also not operate if another function such as a Saving Session or Boost is operational.



