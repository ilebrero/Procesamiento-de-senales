import librosa
import librosa.display

import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

from IPython.display import Audio, display, Image

filename = "./Sine.wav"
y, sr = librosa.load(filename)
# trim silent edges
# audio_trimmed, _ = librosa.effects.trim(y)

# librosa.display.waveplot(audio_trimmed, sr=sr);

n_fft = sr
D = np.abs(librosa.stft(y[:n_fft], n_fft=n_fft, hop_length=n_fft+1))
plt.plot(D)
plt.show()