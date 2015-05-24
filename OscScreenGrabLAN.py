#!/usr/bin/env python
__author__ = 'RoGeorge'
#
# TODO: Add timestamp and mark the trigger point as t0
# TODO: Use channels label instead of chan1, chan2, chan3, chan4, math
# TODO: Add command line parameters file path
# TODO: Add GUI
# TODO: Add browse and custom filename selection
# TODO: Create executable distributions
#
import telnetlib_receive_all
import time
import Image
import StringIO
import sys
import os
import platform

# Update the next lines for your own default settings:
path_to_save = ""
save_format = "PNG"
IP_DS1104Z = "192.168.1.3"

# Rigol/LXI specific constants
port = 5555

expected_len = 1152068
TMC_header_len = 11
terminator_len = 3

big_wait = 10
small_wait = 1

company = 0
model = 1
serial = 2

# Check command line parameters
script_name = os.path.basename(sys.argv[0])


def print_help():
    # Print usage
    print
    print "Usage:"
    print "    " + "python " + script_name + " png|bmp|csv [oscilloscope_IP [save_path]]"
    print
    print "Usage examples:"
    print "    " + "python " + script_name + " png"
    print "    " + "python " + script_name + " csv 192.168.1.3"
    print
    print "The following usage cases are not yet implemented:"
    print "    " + "python " + script_name + " bmp 192.168.1.3 my_place_for_captures"
    print
    print "This program captures either the waveform or the whole screen"
    print "    of a Rigol DS1000Z series oscilloscope, then save it on the computer"
    print "    as a CSV, PNG or BMP file with a timestamp in the file name."
    print
    print "    The program is using LXI protocol, so the computer"
    print "    must have LAN connection with the oscilloscope."
    print "    USB and/or GPIB connections are not used by this software."
    print
    print "    No VISA, IVI or Rigol drivers are needed."
    print

# Read/verify file type
if len(sys.argv) <= 1:
    print_help()
    sys.exit("Warning - wrong command line parameters.")
elif sys.argv[1].lower() not in ["png", "bmp", "csv"]:
    print_help()
    print "This file type is not supported: ", sys.argv[1]
    sys.exit("ERROR")

file_format = sys.argv[1].lower()

# Read IP
if len(sys.argv) > 1:
    IP_DS1104Z = sys.argv[2]

# Create/check if 'path' exists

# Check network response (ping)
if platform.system() == "Windows":
    response = os.system("ping -n 1 " + IP_DS1104Z + " > nul")
else:
    response = os.system("ping -c 1 " + IP_DS1104Z + " > /dev/null")

if response != 0:
    print
    print "No response pinging " + IP_DS1104Z
    print "Check network cables and settings."
    print "You should be able to ping the oscilloscope."

# Open a modified telnet session
# The default telnetlib drops 0x00 characters,
#   so a modified library 'telnetlib_receive_all' is used instead
tn = telnetlib_receive_all.Telnet(IP_DS1104Z, port)
tn.write("*idn?")  # ask for instrument ID
instrument_id = tn.read_until("\n", 1)

# Check if instrument is set to accept LAN commands
if instrument_id == "command error":
    print instrument_id
    print "Check the oscilloscope settings."
    print "Utility -> IO Setting -> RemoteIO -> LAN must be ON"
    sys.exit("ERROR")

# Check if instrument is indeed a Rigol DS1000Z series
id_fields = instrument_id.split(",")
if (id_fields[company] != "RIGOL TECHNOLOGIES") or \
        (id_fields[model][:3] != "DS1") or (id_fields[model][-1] != "Z"):
    print
    print "ERROR: No Rigol from series DS1000Z found at ", IP_DS1104Z
    sys.exit("ERROR")

print "Instrument ID:",
print instrument_id

# Prepare filename as C:\MODEL_SERIAL_YYYY-MM-DD_HH.MM.SS
timestamp = time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime())
filename = path_to_save + id_fields[model] + "_" + id_fields[serial] + "_" + timestamp

if file_format in ["png", "bmp"]:
    # Ask for an oscilloscope display print screen
    tn.write("display:data?")
    print "Receiving screen capture..."
    buff = tn.read_until("\n", big_wait)

    # Just in case the transfer did not complete in the expected time
    while len(buff) < expected_len:
        tmp = tn.read_until("\n", small_wait)
        if len(tmp) == 0:
            break
        buff += tmp

    # Strip TMC Blockheader and terminator bytes
    buff = buff[TMC_header_len:-terminator_len]

    # Save as PNG or BMP according to file_format
    im = Image.open(StringIO.StringIO(buff))
    im.save(filename + "." + file_format, file_format)
    print "Saved file:", filename + "." + file_format

elif file_format == "csv":
    # Put osc in STOP mode
    # tn.write("stop")
    # response = tn.read_until("\n", 1)

    # Scan for displayed channels
    channel_list = []
    for channel in ["chan1", "chan2", "chan3", "chan4", "math"]:
        tn.write(channel + ":display?")
        response = tn.read_until("\n", 1)

        # Strip '\n' terminator
        response = response[:-1]
        if response == '1':
            channel_list += [channel]

    print "Active channels on the display:", channel_list

    csv_buff = ""

    # for each active channel
    for channel in channel_list:
        # Read WAVE parameters

        # Set WAVE parameters
        tn.write("waveform:source " + channel)
        time.sleep(0.2)

        # Maximum - only displayed data when osc. in RUN mode, or full memory data when STOPed
        tn.write("waveform:mode normal")
        time.sleep(0.2)

        tn.write("waveform:format ASCII")
        time.sleep(0.2)

        # Get data
        tn.write("waveform:data?")

        print "Receiving data for channel " + str(channel) + "..."
        buff = tn.read_until("\n", big_wait)

        # Just in case the transfer did not complete in the expected time
        while buff[-1] != "\n":
            tmp = tn.read_until("\n", small_wait)
            if len(tmp) == 0:
                break
            buff += tmp

        # Append each value to csv_buff

        # Strip headers (TMC and points number)
        TMC_header = buff[:TMC_header_len]
        data_points = float(TMC_header[2:])
        # Strip TMC Blockheader and terminator bytes
        buff = buff[TMC_header_len:-1]

        # Process data

        buff_list = buff.split(",")
        buff_rows = len(buff_list)

        # Put red data into csv_buff
        csv_buff_list = csv_buff.split(os.linesep)
        csv_rows = len(csv_buff_list)

        current_row = 0
        if csv_buff == "":
            csv_first_column = True
            csv_buff = str(channel) + os.linesep
        else:
            csv_first_column = False
            csv_buff = str(csv_buff_list[current_row]) + "," + str(channel) + os.linesep

        for point in buff_list:
            current_row += 1
            if csv_first_column:
                csv_buff += str(point) + os.linesep
            else:
                if current_row < csv_rows:
                    csv_buff += str(csv_buff_list[current_row]) + "," + str(point) + os.linesep
                else:
                    csv_buff += "," + str(point) + os.linesep

    # Save data as CSV
    scr_file = open(filename + "." + file_format, "wb")
    scr_file.write(csv_buff)
    scr_file.close()

    print "Saved file:", filename + "." + file_format

tn.close()
