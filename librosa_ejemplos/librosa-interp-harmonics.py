import librosa
import librosa.display
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from os import listdir, mkdir
from os.path import isfile, join, splitext

# Estimate the harmonics of a time-averaged tempogram
def relacion_fundamental_harmonicos(file):
	y, sr = librosa.load(file)
	# y, sr = librosa.load("../audios/clash cymbals/clash-cymbals__long_forte_undamped.mp3")
	h_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	S = np.abs(librosa.stft(y))
	fft_freqs = librosa.fft_frequencies(sr=sr)
	S_harm = librosa.interp_harmonics(S, fft_freqs, h_range, axis=0)

	return np.sum(S_harm[1]) / np.sum(S_harm[2:]) 
	# print(S_harm.shape)
	# (6, 1025, 646)

	# plt.figure()
	# for i, _sh in enumerate(S_harm, 1):
	    # plt.subplot(3, 2, i)
	    # librosa.display.specshow(librosa.amplitude_to_db(_sh,
	                                                    #  ref=S.max()),
	                            #  sr=sr, y_axis='log')
	    # plt.title('h={:.3g}'.format(h_range[i-1]))
	    # plt.yticks([])
	# plt.tight_layout()
	# plt.show()


def getFiles(directory):
	return [filePath for filePath in listdir(directory) if isfile(join(directory, filePath))]

def containsAll(substrings, string):
	res = True
	for s in substrings:
		res = res and (s in string)
	return res


def containsAny(substrings, string):
	res = False
	for s in substrings:
		res = res or (s in string)
	return res

def getConcat(arr):
	res = ""
	for a in arr:
		res = res + "_" + a
	return res

def processTones(directory, substrings, not_substrings, instrument):
	files = getFiles(directory)
	f = open ("resultados_" + instrument + ".csv", 'w')
	f.write("archivo," + getConcat(substrings) + "\n")
	for file in files:
		if containsAll(substrings, file) and not containsAny(not_substrings, file):
			filePath = join(directory, file)
			f.write(file+','+str(relacion_fundamental_harmonicos(filePath)) + "\n")

			# print("### Procesando: " + join(directory, filePath))
			# timeDomain, frecuecyDomain = getWavData(filePath)
			
			# print("### Ploteando: " + join(filePath))
			# createDirIfDoesntExists(join(directory, SAVED_PLOT_DIR))
			# jpgSavedPlotPath = join(directory, SAVED_PLOT_DIR, splitext(file)[0] + JPG_EXTENSION) 
			# savePlotDomains(timeDomain, frecuecyDomain, 10000, jpgSavedPlotPath)
	f.close()

processTones("audios/violin", ["arco", "normal", "fortissimo"], ["trill"], "violin_fortissimo")
# processTones("audios/violin", ["arco", "normal", "pianissimo"], ["trill"], "violin")


# processTones("audios/clash cymbals", [], ["trill"], "clas_symbals")3
# processTones("audios/flute", ["fortissimo", "normal"], ["trill"], "flute")

# "../audios/flute/flute_A5_025_mezzo-forte_normal.mp3"