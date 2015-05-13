# DS1054Z_screen_capture
'OscScreenGrabLAN.py' is a Python script that captures
whatever is displayed by the screen of a Rigol DS1000Z series oscilloscope.
To achieve this, SCPI commands are sent from the computer to the oscilloscope using the LXI protocol.
The computer and the oscilloscope are connected together by a LAN.
No USB, no VISA, no IVI and no drivers are required.
Python 2 is required. Python 3 is not supported.

Tested only with Windows 7, Python 2.7.9 and Rigol DS1104Z (a fully upgraded DS1054Z oscilloscope).

Usage:
------
Connect the computer and the oscilloscope together by LAN. Run 'OscScreenGrabLAN.py' in order to capture an image from the oscilloscope display, and save it to the computer disk.

Example:

    C:\Python27\python.exe OscScreenGrabLAN.py
    
    