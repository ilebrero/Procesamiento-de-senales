library(tuneR)
library(seewave)

plotTimeAndFrecuencyDomains <- function(directory, samples)
{
	sndObj <- readMP3(directory)

	# Uso el canal izquierdo
	s1 <- head(sndObj@left, samples)

	# Adaptando el tamano de los valores para que queden entre (-1, 1) (o es cerrado?)
	s1 <- s1 / 2^(sndObj@bit -1)

	#### Para plotearlo
	timeArray <- (0:(length(s1)-1)) / sndObj@samp.rate
	timeArray <- timeArray * samples #scale to milliseconds

	######

	fft.s1 = fft(s1)

	filtroDF = rep(1, samples)
	# filtroDF [1500:(samples-500)] = 0
	filtroDF [500:(samples-500)] = 0

	fft.s1 = filtroDF * fft.s1 

	#####
	# Ploteo el dominio del tiempo
	retras = Re(fft(fft.s1, inverse=TRUE) / samples)
	plot(timeArray, retras, type='l', col='black', xlab='Time (ms)', ylab='Amplitude')

	# Ploteo el dominio de la frecuencia
	# fft.s1 = fft(s1)
	plot(Mod(fft.s1), type='l')

	# Save result
	saveWav(retras, f=22050)
}


plotTimeAndFrecuencyDomains('audios/Guitarra/Philarmonica/guitar_A2_very-long_forte_normal.mp3', 90000)