import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

filename = '../audios/Violin/violin_A4_025_piano_arco-normal.mp3'
y, sr = librosa.load(filename)
# trim silent edges
whale_song, _ = librosa.effects.trim(y)
librosa.display.waveplot(whale_song, sr=sr)

n_fft = 2048
D = np.abs(librosa.stft(whale_song[:n_fft], n_fft=n_fft,
                        hop_length=n_fft+1))
hop_length = 128
D = np.abs(librosa.stft(whale_song, n_fft=n_fft,
                        hop_length=hop_length))
librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='linear')
plt.colorbar()
plt.show()
