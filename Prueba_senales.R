library(tuneR)
library(seewave) 

shifter <- function(x, n = 1) {
  if (n == 0) x else c(tail(x, -n), head(x, n))
}

plotTimeAndFrecuencyDomains <- function(directory, samples)
{
	sndObj <- readMP3(directory)

	samples <- length(sndObj@left)
	# Uso el canal izquierdo
	s1 <- head(sndObj@left, samples)

	recorte <- 500
	# Adaptando el tamano de los valores para que queden entre (-1, 1) (o es cerrado?)
	s1 <- s1 / 2^(sndObj@bit -1)

	#### Para plotearlo
  timeArray <- (0:(length(s1)-1)) / sndObj@samp.rate
	timeArray <- timeArray * samples #scale to milliseconds

	deltaT <- 1/sndObj@samp.rate
	deltaF <- 1/(samples*deltaT)
	
	freqTimeArray <- (0:(length(s1)-1)) * deltaF
	
	freqTimeArray <- head(freqTimeArray,recorte)
	######

	fft.s1 = fft(s1)

	#fft.s1 = shifter(fft.s1, 1000)

	

	# filtroDF = rep(1, samples)
	# filtroDF [10000:(samples-10000)] = 0
	# # filtroDF [500:(samples-500)] = 0

	# fft.s1 = filtroDF * fft.s1 

	#####
	# Ploteo el dominio del tiempo
	retras = Re(fft(fft.s1, inverse=TRUE) / samples)
	plot(timeArray, retras, type='l', col='black', xlab='Time (ms)', ylab='Amplitude')

	# Ploteo el dominio de la frecuencia
	# fft.s1 = fft(s1)
	plot(freqTimeArray,Mod(head(fft.s1,recorte)), type='l')

	# Save result
	savewav(retras, f=sndObj@samp.rate)
}




plotTimeAndFrecuencyDomains('audios/trumpet/trumpet_A4_05_forte_normal.mp3', 90000)

