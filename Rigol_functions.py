__author__ = 'RoGeorge'

import time
import pip
import sys
import logging


def print_running_Python_versions():
    print "Running Python version:"
    print (sys.version)  # parentheses necessary in python 3.
    print sys.version_info
    print

    installed_packages = pip.get_installed_distributions()
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
    print "Installed Python modules:"
    print(installed_packages_list)
    print


def command(tn, SCPI):
    logging.info("SCPI to be sent: " + SCPI)
    answer_wait_s = 1
    response = ""
    while response != "1\n":
        tn.write("*OPC?")  # previous operation(s) has completed ?
        logging.info("Send SCPI: *OPC?")
        response = tn.read_until("\n", 1)  # wait max 1s for an answer
        logging.info("Received response: " + response)

    tn.write(SCPI)
    logging.info("Sent SCPI: " + SCPI)
    response = tn.read_until("\n", answer_wait_s)
    logging.info("Received response: " + response)
    return response


def get_memory_depth(tn):
    # Define number of horizontal grid divisions for DS1054Z
    h_grid = 12

    # ACQuire:MDEPth
    mdep = command(tn, "ACQ:MDEP?")

    # if mdep is "AUTO"
    if mdep == "AUTO\n":
        # ACQuire:SRATe
        srate = command(tn, "ACQ:SRAT?")

        # TIMebase[:MAIN]:SCALe
        scal = command(tn, "TIM:SCAL?")

        # mdep = h_grid * scal * srate
        mdep = h_grid * scal * srate

    # return mdep
    return int(mdep)


# return maximum achieved stop point, or 0 for wrong input parameters
# if achieved == requested, then set the start and stop waveform as n1_d and n2_d
def is_waveform_from_to(tn, n1_d, n2_d):
    # read current
    # WAVeform:STARt
    n1_c = int(command(tn, "WAV:STAR?"))

    # WAVeform:STOP
    n2_c = int(command(tn, "WAV:STOP?"))

    if (n1_d > n2_d) or (n1_d < 1) or (n2_d < 1):
        # wrong parameters
        return 0

    elif n2_d < n1_c:
        # first set n1_d then set n2_d

        print "a ", "n1_d=", n1_d, "n2_d=", n2_d
        command(tn, "WAV:STAR " + str(n1_d))
        command(tn, "WAV:STOP " + str(n2_d))

    else:
        # first set n2_d then set n1_d
        print "b ", "n2_d", n2_d, "n1_d=", n1_d
        command(tn, "WAV:STOP " + str(n2_d))
        command(tn, "WAV:STAR " + str(n1_d))

    # read achieved n2
    n2_a = int(command(tn, "WAV:STOP?"))

    if n2_a < n2_d:
        # restore n1_c, n2_c
        is_waveform_from_to(tn, n1_c, n2_c)

    # return n2_a
    return n2_a
