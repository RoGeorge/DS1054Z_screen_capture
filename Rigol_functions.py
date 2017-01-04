import pip
import sys
import logging

__author__ = 'RoGeorge'


def log_running_python_versions():
    logging.info("Python version: " + str(sys.version) + ", " + str(sys.version_info))  # () required in Python 3.

    installed_packages = pip.get_installed_distributions()
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
    logging.info("Installed Python modules: " + str(installed_packages_list))


def command(tn, scpi):
    logging.info("SCPI to be sent: " + scpi)
    answer_wait_s = 1
    response = ""
    while response != "1\n":
        tn.write("*OPC?\n")  # previous operation(s) has completed ?
        logging.info("Send SCPI: *OPC? # May I send a command? 1==yes")
        response = tn.read_until("\n", 1)  # wait max 1s for an answer
        logging.info("Received response: " + response)

    tn.write(scpi + "\n")
    logging.info("Sent SCPI: " + scpi)
    response = tn.read_until("\n", answer_wait_s)
    logging.info("Received response: " + response)
    return response


# first TMC byte is '#'
# second is '0'..'9', and tells how many of the next ASCII chars
#   should be converted into an integer.
#   The integer will be the length of the data stream (in bytes)
# after all the data bytes, the last char is '\n'
def tmc_header_bytes(buff):
    return 2 + int(buff[1])


def expected_data_bytes(buff):
    return int(buff[2:tmc_header_bytes(buff)])


def expected_buff_bytes(buff):
    return tmc_header_bytes(buff) + expected_data_bytes(buff) + 1


def get_memory_depth(tn):
    # Define number of horizontal grid divisions for DS1054Z
    h_grid = 12

    # ACQuire:MDEPth
    mdep = command(tn, ":ACQ:MDEP?")

    # if mdep is "AUTO"
    if mdep == "AUTO\n":
        # ACQuire:SRATe
        srate = command(tn, ":ACQ:SRAT?")

        # TIMebase[:MAIN]:SCALe
        scal = command(tn, ":TIM:SCAL?")

        # mdep = h_grid * scal * srate
        mdep = h_grid * float(scal) * float(srate)

    # return mdep
    return int(mdep)
