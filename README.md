# DS1054Z_screen_capture
'OscScreenGrabLAN.py' is a Python script that captures
whatever is displayed on the screen of a Rigol DS1000Z series oscilloscope.

It can save data as a WYSIWYG (What You See Is What You Get) picture of the oscilloscope screen,
 or as a text file in CSV (Comma Separated Values) format.

To achieve this, SCPI (Standard Commands for Programmable Instruments) are sent from the computer
to the oscilloscope, using the LXI (LAN-based eXtensions for Instrumentation) protocol over a Telnet connection.
The computer and the oscilloscope are connected together by a LAN (Local Area Network).
No USB (Universal Serial Bus), no VISA (Virtual Instrument Software Architecture),
no IVI (Interchangeable Virtual Instrument) and no Rigol drivers are required.
Python 2 is required. Python 3 is not supported.

Tested with Windows 10, Python 2.7.12, pillow and Rigol DS1104Z (a fully upgraded DS1054Z oscilloscope).
Tested with Linux Ubuntu 16.04.1, Python 2.7.12 and pillow.


User Manual:
-----------
This program captures either the waveform or the whole screen
    of a Rigol DS1000Z series oscilloscope, then save it on the computer
    as a CSV, PNG or BMP file with a timestamp in the file name.

    The program is using LXI protocol, so the computer
    must have LAN connection with the oscilloscope.
    USB and/or GPIB connections are not used by this software.

    No VISA, IVI or Rigol drivers are needed.
	
Installation:

    Installation on a clean Windows 10 machine
	    1. download and install Python 2.7.12 from https://www.python.org/downloads/
		2. to install pillow, open a Command Prompt and type
		    pip install pillow
		3. download and unzip 'DS1054Z_screen_capture-master.zip' from https://github.com/RoGeorge/DS1054Z_screen_capture
		4. connect the oscilloscope to the LAN (in this example, the oscilloscope have fix IP=192.168.1.3)
		5. in the Command Prompt, change the directory (CD) to the path were 'OscScreenGrabLAN.py' was un-zipped
		    cd path_where_the_OscScreenGrabLAN.py_was_unzipped
		6. to run the OscScreenGrabLAN.py in the Command Prompt, type
		    python OscScreenGrabLAN.py png 192.168.1.3
			
	Installation on a clean Ubuntu 16.04.1
	    1. Python is already installed in Ubuntu 16.04.1 desktop
	    2. to install pillow, open a Terminal and type:
		    sudo add-apt-repository universe
			sudo apt-get update
			sudo apt-get install python-pip
			pip install pillow
		3. download and unzip 'DS1054Z_screen_capture-master.zip' from https://github.com/RoGeorge/DS1054Z_screen_capture
		4. connect the oscilloscope to the LAN (in this example, the oscilloscope have fix IP=192.168.1.3)
		5. in the Terminal, change the directory (CD) to the path were 'OscScreenGrabLAN.py' was un-zipped
		    cd path_where_the_OscScreenGrabLAN.py_was_unzipped
		6. to run the OscScreenGrabLAN.py in the Terminal, type
		    python OscScreenGrabLAN.py png 192.168.1.3			
	
Other usages syntax:

    python OscScreenGrabLAN.py png|bmp|csv oscilloscope_IP

Usage examples:

    python OscScreenGrabLAN.py png 192.168.1.3
    python OscScreenGrabLAN.py csv 192.168.1.3





    