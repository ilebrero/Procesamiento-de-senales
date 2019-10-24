library(tuneR)
library(seewave) 

shifter <- function(x, n = 1) {
  if (n == 0) x else c(tail(x, -n), head(x, n))
}

obtenerSamples <- function(audioFile, samples)
{
	# Levantar el archivo y sacar la data de adentro
	samples <- length(audioFile@left)
	print(samples)
	# Uso el canal izquierdo
	s1 <- head(audioFile@left, samples)

	s1
}

obtenerDominioFrecuencias <- function(audioFile, s1, samples, recorte)
{
	deltaT <- 1/audioFile@samp.rate
	deltaF <- 1/(samples*deltaT)
	
	freqTimeArray <- (0:(length(s1)-1)) * deltaF
	freqTimeArray <- head(freqTimeArray,recorte)

	freqTimeArray
}

obtenerExperimento1 <- function(fft, posFundamental)
{
	# cortamos la series para serpara el ruido del final
	largoMitad <- length(fft)/4

	# Debug
	print("asdasds")
	print(posFundamental)
	print(length(head(Mod(fft),largoMitad)))
	print(length(tail(head(Mod(fft),largoMitad),largoMitad-(posFundamental*1.5))))

  	### Sumamos las cosas que ya conocemos
	sumaEnergias <- sum(tail(head(Mod(fft),posFundamental*1.25),posFundamental))
 	sumaEnergiasArmonicos <- sum(tail(head(Mod(fft),largoMitad),largoMitad-(posFundamental*1.25)))
	

	energiaTotal <- sumaEnergiasArmonicos / sumaEnergias * 100
	
	print(energiaTotal)
}

plotTimeAndFrecuencyDomains <- function(directory, samples, posFundamental)
{
	audioFile <- readMP3(directory)

	s1 <- obtenerSamples(audioFile, samples)
	# Levantar el archivo y sacar la data de adentro

	# TODO: Ponerlo como param
	recorte <- 10000
	# Adaptando el tamano de los valores para que queden entre (-1, 1) (o es cerrado?)
	s1 <- s1 / 2^(audioFile@bit -1)


	#### Armamos los dominios
  	timeArray <- (0:(length(s1)-1)) / audioFile@samp.rate
	timeArray <- timeArray * samples #scale to milliseconds

	### Obtener para las frecuencias
	freqTimeArray <-obtenerDominioFrecuencias(audioFile, s1, samples, recorte)

	# Calculamos la transformada de fourier
	fft.s1 = fft(s1)

	# Experimento shifteando los valores
	#fft.s1 = shifter(fft.s1, 1000)
	
	### Experimento1: Sumar los harmonicos y ver si tinenen relacion con la fundamental
	obtenerExperimento1 <- obtenerExperimento1(fft.s1, posFundamental)

	# filtroDF = rep(1, samples)
	# filtroDF [10000:(samples-10000)] = 0
	# # filtroDF [500:(samples-500)] = 0

	# fft.s1 = filtroDF * fft.s1 

		#### Ploteos y otros

	#####
	# Ploteo el dominio del tiempo
	retras = Re(fft(fft.s1, inverse=TRUE) / samples)
	#plot(timeArray, retras, type='l', col='black', xlab='Time (ms)', ylab='Amplitude')

	# Ploteo el dominio de la frecuencia
	# fft.s1 = fft(s1)
  # TODO: Armar un vector / en la posicion 440 tenga la energia de la frecuencia 440
	      # Lo vamos a usar para calcular la energia de toda la frecuencia y comparar la energia de la fundamental vs los armonicos.
	plot(freqTimeArray,Mod(head(fft.s1,recorte)), type='l')

	# Save result
	savewav(retras, f=audioFile@samp.rate)
}




plotTimeAndFrecuencyDomains('audios/trumpet/trumpet_A4_05_forte_normal.mp3', 90000, 440)
plotTimeAndFrecuencyDomains('audios/violin/violin_A4_025_mezzo-forte_arco-normal.mp3', 90000, 440)

