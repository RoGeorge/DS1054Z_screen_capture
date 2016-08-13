__author__ = 'RoGeorge'

import time

def get_memory_depth(tn):
	# Define number of horizontal grid divisions for DS1054Z
	h_grid = 12

	# ACQuire:MDEPth
	tn.write("ACQ:MDEP?")
	mdep = tn.read_until("\n", 1)

	# if mdep is "AUTO"
	if mdep == "AUTO\n":
		# ACQuire:SRATe
		tn.write("ACQ:SRAT?")
		srate = tn.read_until("\n", 1)

		# TIMebase[:MAIN]:SCALe
		tn.write("TIM:SCAL?")
		scal = tn.read_until("\n", 1)

		# mdep = h_grid * scal * srate
		mdep = h_grid * float(scal) * float(srate)

	# return mdep
	return float(mdep)


# return maximum achieved stop point, or 0 for wrong input parameters
# if achieved == requested, then set the start and stop waveform as n1_d and n2_d
def is_waveform_from_to(tn, n1_d, n2_d):
	# read current
	# WAVeform:STARt
	tn.write("WAV:STAR?")
	n1_c = float(tn.read_until("\n", 1))

	# WAVeform:STOP
	tn.write("WAV:STOP?")
	n2_c = float(tn.read_until("\n", 1))

	if (n1_d > n2_d) or (n1_d < 1) or (n2_d < 1):
		# wrong parameters
		return 0

	elif n2_d < n1_c:
		# first set n1_d then set n2_d
		tn.write("WAV:STAR " + str(n1_d))
		time.sleep(1)
		tn.write("WAV:STOP " + str(n2_d))
		time.sleep(1)

	else:
		# first set n2_d then set n1_d
		tn.write("WAV:STOP " + str(n2_d))
		time.sleep(1)
		tn.write("WAV:STAR " + str(n1_d))
		time.sleep(1)

	# read achieved n2
	tn.write("WAV:STOP?")
	n2_a = float(tn.read_until("\n", 1))

	if n2_a < n2_d:
		# restore n1_c, n2_c
		is_waveform_from_to(tn, n1_c, n2_c)

	# return n2_a
	return n2_a


