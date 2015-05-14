__author__ = 'RoGeorge'
#
# TODO: Port for Linux
# TODO: Add command line parameters for IP, file path and file format
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

# Check parameters
script_name = os.path.basename(sys.argv[0])

# Print usage
print
print "Usage:"
print "    " + script_name + " [oscilloscope_IP [save_path [PNG | BMP]]]"
print
print "Usage examples:"
print "    " + script_name
print "    " + script_name + " 192.168.1.3"
print "    " + script_name + " 192.168.1.3 my_place_for_osc_captures"
print "    " + script_name + " 192.168.1.3 my_place_for_osc_captures BMP"
print
print "This program capture the image displayed"
print "    by a Rigol DS1000Z series oscilloscope, then save it on the computer"
print "    as a PNG or BMP file with a timestamp in the file name."
print
print "    The program is using LXI protocol, so the computer"
print "    must have LAN connection with the oscilloscope."
print "    USB and/or GPIB connections are not used by this software."
print
print "    No VISA, IVI or Rigol drivers are needed."
print

# Create/check if 'path' exists


# Check network response (ping)
response = os.system("ping -n 1 " + IP_DS1104Z + " > nul")
if response != 0:
	print
	print "No response pinging " + IP_DS1104Z
	print "Check network cables and settings."
	print "You should be able to ping the oscilloscope."

# Open a modified telnet session
# The default telnetlib drops 0x00 characters,
#   so a modified library 'telnetlib_receive_all' is used instead
tn = telnetlib_receive_all.Telnet(IP_DS1104Z, port)
tn.write("*idn?")                       # ask for instrument ID
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

print "Instrument ID:"
print instrument_id

# Prepare filename as C:\MODEL_SERIAL_YYYY-MM-DD_HH.MM.SS
timestamp = time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime())
filename = path_to_save + id_fields[model] + "_" + id_fields[serial] + "_" + timestamp

# Ask for an oscilloscope display print screen
tn.write("display:data?")
print "Receiving..."
buff = tn.read_until("\n", big_wait)

# Just in case the transfer did not complete in 10 seconds
while len(buff) < expected_len:
	tmp = tn.read_until("\n", small_wait)
	if len(tmp) == 0:
		break
	buff += tmp

# Strip TMC Blockheader and terminator bytes
buff = buff[TMC_header_len:-terminator_len]

# Save as PNG
im = Image.open(StringIO.StringIO(buff))
im.save(filename + ".png", "PNG")
print "Saved file:", filename + ".png"

# Save as BMP
# scr_file = open(filename + ".bmp", "wb")
# scr_file.write(buff)
# scr_file.close()

tn.close()
