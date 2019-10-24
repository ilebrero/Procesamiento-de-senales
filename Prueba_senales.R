library(tuneR)
library(seewave) 

shifter <- function(x, n = 1) {
  if (n == 0) x else c(tail(x, -n), head(x, n))
}

obtenerSamples <- function(audioFile, samples)
{
	# Levantar el archivo y sacar la data de adentro
	samples <- length(audioFile@left)
	
	# Uso el canal izquierdo
	s1 <- head(audioFile@left, samples)

	# Adaptando el tamano de los valores para que queden entre (-1, 1) (o es cerrado?)
	s1 <- s1 / 2^(audioFile@bit -1)


	s1
}


obtenerDominoTiempo <- function(audioFile, s1, samples)
{
  	timeArray <- (0:(length(s1)-1)) / audioFile@samp.rate
	timeArray <- timeArray * samples #scale to milliseconds

	timeArray
}

obtenerDominioFrecuencias <- function(audioFile, s1, samples)
{
	deltaF <- audioFile@samp.rate / samples
	freqTimeArray <- (0:(length(s1)-1)) * deltaF
	freqTimeArray
}


filtrarBanda <- function(fft, midPoint, delta)
{
	tail(
		head(
			Mod(fft),
			midPoint + delta
		),
		delta * 2
	)
}


## Podemos buscar la frecuencia fundamental de un audio para predecir que nota es (o que instrumento?)
obtenerExperimento2 <- function()
{
	# TODO
} 

obtenerExperimento1 <- function(fft, posFundamental)
{
	# cortamos la series para serpara el ruido del final
	fftEfectiva <- head(fft, length(fft)/2)

	# Cortamos desde posFundamental como centro 1.25 para cada lado
	frecFundamental <- filtrarBanda(fftEfectiva, posFundamental, posFundamental*1.25)

	# Cortamos desde el final de la fundamental hasta el final (todos los armonicos)
	frecHarmonicos  <- tail(fftEfectiva, length(fftEfectiva)-(posFundamental*1.25))  

	# elevamos al cuadrado para calcular la energia (Ver diapos)
	frecFundamental <- Mod(frecFundamental) * Mod(frecFundamental)
	frecHarmonicos <- Mod(frecHarmonicos) * Mod(frecHarmonicos)

	sumaEnergias <- sum(frecFundamental)
	sumaEnergiasArmonicos = sum(frecHarmonicos)

	print(sumaEnergias)
	print(sumaEnergiasArmonicos)

	energiaTotal <- sumaEnergiasArmonicos / sumaEnergias * 100
	
	print(energiaTotal)
}

plotTimeAndFrecuencyDomains <- function(directory, samples, posFundamental, recorte)
{
	audioFile <- readMP3(directory)

	s1 <- obtenerSamples(audioFile, samples)

	#### Armamos los dominios
	timeArray <- obtenerDominoTiempo(audioFile, s1, samples)

	### Obtener para las frecuencias
	freqTimeArray <-obtenerDominioFrecuencias(audioFile, s1, samples)

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
	plot(head(timeArray, recorte), head(retras, recorte), type='l', col='black', xlab='Time', ylab='Amplitude')

	# Ploteo el dominio de la frecuencia
	# fft.s1 = fft(s1)
  # TODO: Armar un vector / en la posicion 440 tenga la energia de la frecuencia 440
	      # Lo vamos a usar para calcular la energia de toda la frecuencia y comparar la energia de la fundamental vs los armonicos.
	plot(head(freqTimeArray, recorte),Mod(head(fft.s1,recorte)), type='l')

	# Save result
	savewav(retras, f=audioFile@samp.rate)
}




# plotTimeAndFrecuencyDomains('audios/trumpet/trumpet_A4_05_forte_normal.mp3', 90000, 440, 100000)
plotTimeAndFrecuencyDomains('audios/flute/flute_A5_05_pianissimo_normal.mp3', 90000, 440, 100000)
# plotTimeAndFrecuencyDomains('audios/violin/violin_A4_025_mezzo-forte_arco-normal.mp3', 90000, 440, 100000)

