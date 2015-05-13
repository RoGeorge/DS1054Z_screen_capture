# DS1054Z_screen_capture
'OscScreenGrabLAN.py' is a Python script that captures
whatever is displayed on the screen of a Rigol DS1000Z series oscilloscope.
To achieve this, SCPI (Standard Commands for Programmable Instruments) are sent from the computer
to the oscilloscope, using the LXI (LAN-based eXtensions for Instrumentation) protocol over a Telnet connexion.
The computer and the oscilloscope are connected together by a LAN (Local Area Network).
No USB (Universal Serial Bus), no VISA (Virtual Instrument Software Architecture),
no IVI (Interchangeable Virtual Instrument) and no Rigol drivers are required.
Python 2 is required. Python 3 is not supported.

Tested only with Windows 7, Python 2.7.9 and Rigol DS1104Z (a fully upgraded DS1054Z oscilloscope).

Usage:
------
Install Python 2.7.9 from 'https://www.python.org/downloads'.
Connect together the computer and the oscilloscope (by LAN).
In order to capture an image from the oscilloscope display and save it to the computer disk,
open a Command Prompt as Administrator and run 'OscScreenGrabLAN.py'.

Example:

    C:\Python27\python.exe OscScreenGrabLAN.py
    
    