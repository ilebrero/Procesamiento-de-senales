import librosa

def audioSpectrumCentroid(signal, sampling_rate):
	S_pow = librosa.feature.melspectogram(y=signal, sr=sampling_rate)


def generate_spectral_rolloff(signal, sampling_rate):
	return np.array(
		librosa.feature.spectral_rolloff(signal, sampling_rate)
	)

def generate_audio_special_features(signal, sampling_rate):
	generate_spectral_rollout(signal, sampling_rate)