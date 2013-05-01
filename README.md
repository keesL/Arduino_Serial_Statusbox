Arduino_Serial_Statusbox
========================
Author: Kees Leune <kees@leune.org>
First published: April 30, 2013

A box with red, amber, green LEDs to indicate a status. Controlled via serial port.
I built this project to connect a box that resembles a traffic light via a TCP/IP.
I use it in conjunction with network monitoring software to alert me in case there
are anomalies.

The concept is as follows:

Network client(s) <----> | Network server <> Serial Port | <----> Status Box

The status box can light up any combination of the three LEDs.

In this folder, you will find the following files:

README.md			   - This file
tld.py	               - Traffic Light Daemon
tl_blink.py            - Demonstration client for tld.py that will let all LEDs blink
tl_demo.py   	       - Demonstration client that implements a light show
tl_splunk_connector.py - Script to be called from a Splunk alert to active a status light

traffic_light.ino	   - Arduino Sketch

The files ending in .py are written in Python. The file ending in .ino is an Arduino Uno sketch.

Traffic Light Protocol
----------------------
The traffic light daemon implements a very simple traffic light protocol. 
On startup, tld.py binds to a port that is configured in the file. The following 
commands are understood. Commands are not case sensitive

red on		- turn the red light on
red off     - turn the red light off
amber on    - turn the amber light on
amber off   - turn the amber light off
green on    - turn the green light on
green off   - turn the green light off
status      - display a status of all LEDs
state 0-7   - set state 0-7. State is a binary flag.
				bit 1	= red on   (value: 1)
				bit 2	= amber on (value: 2)
				bit 3	= green on (value: 4)
			  To determine the state for your desired combination of LEDs, just add the
			  listed values. For example, if you want green and red on, and amber off, you
			  would set state 5. To turn off LEDs off, set state 0
quit		- disconnect from the server

Note: there really isn't any worth error handling to speak of. Unexpected input may crash
the daemon.

The deamon will return a value after each command. The first part of the result is always a
numerical code. The following codes are supported:

100  Client connection accepted
101  New state accepted
102  Current status is ...
999  Goodbye

Building the schematic: hints
------------------------------

Take an external power source into a 7805 to get a clean 5V. Using an M-type panel mount bus jack
worked very well for me. I built two small perfboard panels: one for the microcontroller and its
peripherals and one for a 7404 to convert RS232 serial voltages to 5V TTL levels. The low intensity
green LED is just to make sure that the microcontroller started up and that it is doing something.
Feel free to omit it.

Wire up the microcontroller board

Connect inner lead of M-jack to left-most pin of 7805 (Vin)
Connect outer lead of M-jack to middle pin of 7805 (Ground)
The right-most pin of the 7805 is your +5V. 

Arduino Uno processor (Atmel 328)
Pin 1:	 10K resistor to 5V
Pin 2: 	 To serial panel
Pin 3:   To serial panel
Pin 4:   220 ohm resistor to 5mm high intensity red LED anode (long leg)
Pin 5:   220 ohm resistor to 5mm high intensity amber LED anode (long leg)
Pin 6:   220 ohm resistor to 5mm high intensity green LED anode (long leg)
Pin 7:	 +5V
Pin 8:   Ground
Pin 9:   16 MHz crystal
Pin 10:  16 MHz crystal
Pin 20:  +5V
Pin 22:  Ground
Pin 28:  220 ohm resistor to 3mm low intensity green LED anode (long leg)

Connect all the short legs of the LEDs (kathodes) together and link up with other ground leads.
Link all +5V pins together.

On your serial panel:

Pin 1: Connect to serial port pin 3 (assuming DB-9)
Pin 2: Connect to microprocessor port 2
Pin 3: Connect to microprocessor port 3
Pin 4: Connect to serial port pin 2 (assuming DB-9)
Pin 7:  Ground
Pin 14: +5V

Also, connect pin 5 on the DB-9 serial connector to Ground. Make sure all +5V and all Ground are 
connected.

Note that is it practice to use a male DB-9 connector on stuff that you want to connect to a PC. Most
serial cables are female-to-female. YMMV.

It is probably a good idea to place some capacitors over the Vin and Vout on the 7805, as well
as over the leads of the crystal. The other side of the capacitor should connect to ground.

Instructions for building the basic frame of this board can be found on http://dev.arduino.cc/wiki/en/Main/Standalone#toc8