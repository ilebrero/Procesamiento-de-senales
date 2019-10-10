library(tuneR)
library(seewave) 

shifter <- function(x, n = 1) {
  if (n == 0) x else c(tail(x, -n), head(x, n))
}

plotTimeAndFrecuencyDomains <- function(directory, samples, offset, frecOffset)
{
	sndObj <- readMP3(directory)

	samples <- length(sndObj@left)
	# Uso el canal izquierdo
	s1 <- head(sndObj@left, samples)
	s1 <- tail(s1, offset)
	# s1 <- tail(s1

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




# Experimento 1
plotTimeAndFrecuencyDomains('audios/trumpet/trumpet_A2_long_pianissimo_normal.mp3', 30000, 30000, 2500)

# Expe 2
# plotTimeAndFrecuencyDomains('audios/trumpet/trumpet_A4_05_forte_normal.mp3', 30000, 30000, 200)

# expe 3
# plotTimeAndFrecuencyDomains('audios/violin/violin_A4_05_forte_arco-normal.mp3', 30000, 200, 1200)
# Mirar despues: 
#	- Ver el tiempo de los ciclos | podemos ver 1/blabuscar la cuenta) que deberia darnos la frecuencia
#   - Ver que por nota el periodo deberia ser el mismo

# 
# plotTimeAndFrecuencyDomains('audios/trumpet/trumpet_A4_05_forte_normal.mp3', 30000, 15000, 1000)

# Experimento 5
plotTimeAndFrecuencyDomains('audios/trumpet/trumpet_A4_05_forte_normal.mp3', 90000, 90000, 2500)

