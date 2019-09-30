library(tuneR)

plotTimeAndFrecuencyDomains <- function(directory, samples)
{
	sndObj <- readWave(directory)

	# Uso el canal izquierdo
	s1 <- head(sndObj@left, samples)

	# Adaptando el tamano de los valores para que queden entre (-1, 1) (o es cerrado?)
	s1 <- s1 / 2^(sndObj@bit -1)

	#### Para plotearlo
	timeArray <- (0:(length(s1)-1)) / sndObj@samp.rate
	timeArray <- timeArray * samples #scale to milliseconds

	# Ploteo el dominio del tiempo
	plot(timeArray, s1, type='l', col='black', xlab='Time (ms)', ylab='Amplitude')

	# Ploteo el dominio de la frecuencia
	fft.s1 = fft(s1)
	plot(Mod(fft.s1), type='l')
}

plotTimeAndFrecuencyDomains('audios/Bajo/Tonos puros/A_55.000.wav', 1000)