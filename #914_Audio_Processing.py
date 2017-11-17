############################################################################
#																		   #
#			             Musical Note Identification			           #
#																		   #
############################################################################

import numpy as np
import struct
import wave

#Teams can add other helper functions
#which can be added here


sampling_freq = 44100	# Sampling frequency of audio signal

def play(sound_file):
	'''
	sound_file-- a single test audio_file as input argument
	
	#add your code here
	'''
	file_length = sound_file.getnframes()
	sound = np.zeros(file_length)
	for i in range(file_length):
		data = sound_file.readframes(1)
		data = struct.unpack("<h", data)
		sound[i] = int(data[0])
	sound = np.divide(sound, float(2**15))
	sound_length = len(sound)
	window_size = 0.05 # in seconds
	window_length = window_size * sampling_freq
	threshold = 0.05
	silence = [] # initialize list to store silence times
	Identified_Notes = []
	notes = {1046.5: 'C6', 1174.66: 'D6', 1318.51: 'E6', 1396.91: 'F6', 1567.98: 'G6', 1760.00: 'A6', 1975.53: 'B6', 2093.00: 'C7', 2349.32: 'D7', 2637.02: 'E7', 2793.83: 'F7', 3135.96: 'G7', 3520.00: 'A7', 3951.07: 'B7', 4186.01: 'C8', 4698.63: 'D8', 5274.04: 'E8', 5587.65: 'F8', 6271.93: 'G8', 7040.00: 'A8', 7902.13: 'B8'}
	freq_list = list(notes.keys())

	# STATES 0 - Starting State, 1 - Detected Silence, 2 - Detected Note

	# Note Detected after silence = First sample of note
	# Silence Detected after note = Last sample of note

	init = 0 # First Sample of Note Index
	fin = 0 # Last Sample of Note Index
	STATE = 0
	for i in range(0, int(sound_length - window_length)):
		ampl_rms = np.sum(pow(sound[i: i + int(window_length)],2))
		if STATE == 0: # Init
			if (np.sqrt(ampl_rms) <= threshold): 
				STATE = 1
			else:
				STATE = 2
		elif STATE == 1: 
			if ampl_rms <= threshold:					# Detected Silence Again
				STATE = 1 
			else:										# Detected Note
				init = i + window_length                # Set First Sample to current index
				STATE = 0
		elif STATE == 2:
			if ampl_rms <= threshold:   				# Silence Detected
				fin = i 								# Set Last Sample to current index
				STATE = 1
				# Find Frequency
				fourier = np.fft.fft(sound[int(init):int(fin)])
				fourier = np.absolute(fourier)
				indexes = np.argsort(fourier)
				frequency = min(indexes[-1], indexes[-2]) * sampling_freq / len(sound[int(init):int(fin)])
				# Find Note
				best_fit = freq_list[0]
				for freq in freq_list:
					if abs(freq - frequency) < abs(best_fit - frequency):
						best_fit = freq
				Identified_Notes.append(notes[best_fit])
			else:					    # Note Detected Again
				STATE = 2
				
	return Identified_Notes

############################## Read Audio File #############################

if __name__ == "__main__":
	#code for checking output for single audio file
	sound_file = wave.open('Test_Audio_files/Audio_5.wav', 'r')
	Identified_Notes = play(sound_file)
	# print ("Notes = ", Identified_Notes)


	## Changed the below code for better presentation
	#code for checking output for all images
	Identified_Notes_list = []
	for file_number in range(1,6):
		file_name = "Test_Audio_files/Audio_"+str(file_number)+".wav"
		sound_file = wave.open(file_name)
		Identified_Notes = play(sound_file)
		Identified_Notes_list.append(Identified_Notes)
		print ("Notes in Audio_"+str(file_number)+".wav: " + Identified_Notes)    


