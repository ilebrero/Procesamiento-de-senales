import matplotlib.pyplot as plt
import numpy as np

from os import listdir, mkdir
from os.path import isfile, join, splitext
from scipy.io import wavfile as wav
from scipy.fftpack import fft
from enum import Enum

class Instrumento(Enum):
	BAJO     = 1
	VIOLIN   = 2
	GUITARRA = 3

JPG_EXTENSION  = '.jpg'
SAVED_PLOT_DIR = 'plots'

DIRECTORIES = {
	Instrumento.BAJO 	  : 'audios/Bajo',
	Instrumento.VIOLIN   : 'audios/Violin', 
	Instrumento.GUITARRA : 'audios/Guitarra' 
}

DIRECTORIES_TONOS_PUROS = {
	Instrumento.BAJO 	  : 'audios/Bajo/Tonos puros',
	Instrumento.VIOLIN   : 'audios/Violin/Tonos puros', 
	Instrumento.GUITARRA : 'audios/Guitarra/Tonos puros' 
}

def getWavData(filename):
	rate, timeDomainData = wav.read(filename)
	FrecuencyDomainData = fft(timeDomainData)
	return timeDomainData, FrecuencyDomainData

def plotDomains(timeDomainData, FrecuencyDomainData, takenSamples):
	x_axys = np.arange(len(timeDomainData))

	#plot time domain
	plt.subplot(2, 1, 1)
	plt.plot(timeDomainData[:takenSamples])

	#plot frecuency domain
	plt.subplot(2, 1, 2)
	plt.plot(timeDomainData, np.abs(FrecuencyDomainData))

	plt.show()
	plt.clf()

def savePlotDomains(timeDomainData, FrecuencyDomainData, takenSamples, filePath):
	x_axys = np.arange(len(timeDomainData))

	#plot time domain
	plt.subplot(2, 1, 1)
	plt.plot(timeDomainData[:takenSamples])

	#plot frecuency domain
	plt.subplot(2, 1, 2)
	plt.plot(timeDomainData, np.abs(FrecuencyDomainData))


	print("guardando: " + filePath)
	plt.savefig(filePath)
	plt.clf()

def getFiles(directory):
	return [filePath for filePath in listdir(directory) if isfile(join(directory, filePath))]

def createDirIfDoesntExists(directory):
	try:
		mkdir(directory)
		print("creado: " + directory)

	except FileExistsError:
		print("Ya existia el directorio")

def processTones(directory):
	files = getFiles(directory)
	
	for file in files:
		filePath = join(directory, file)
		print("### Procesando: " + join(directory, filePath))
		timeDomain, frecuecyDomain = getWavData(filePath)
		
		print("### Ploteando: " + join(filePath))
		createDirIfDoesntExists(join(directory, SAVED_PLOT_DIR))
		jpgSavedPlotPath = join(directory, SAVED_PLOT_DIR, splitext(file)[0] + JPG_EXTENSION) 
		savePlotDomains(timeDomain, frecuecyDomain, 10000, jpgSavedPlotPath)

for instrumento in Instrumento:
	print("## Procesando el instrumento: " + Instrumento.BAJO.name)
	processTones(DIRECTORIES_TONOS_PUROS[instrumento])
	print("----------------------------------------- \n\n")

# bajoTDD, bajoFDD = getWavData(DIR_BAJO)
# #plotDomains(bajoTDD, bajoFDD, 10000)

# violinTDD, violinFDD = getWavData(DIR_VIOLIN)
# #plotDomains(violinTDD, violinFDD, 10000)

# guitarraTDD, guitarraFDD = getWavData(DIR_GUITARRA)
# plotDomains(guitarraTDD, guitarraFDD, 10000)