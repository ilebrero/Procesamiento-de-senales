import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


# Estimate the harmonics of a time-averaged tempogram

y, sr = librosa.load("../audios/flute/flute_A5_025_mezzo-forte_normal.mp3")
# y, sr = librosa.load("../audios/clash cymbals/clash-cymbals__long_forte_undamped.mp3")
h_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
S = np.abs(librosa.stft(y))
fft_freqs = librosa.fft_frequencies(sr=sr)
S_harm = librosa.interp_harmonics(S, fft_freqs, h_range, axis=0)
print(S_harm.shape)
# (6, 1025, 646)

# plt.figure()
# for i, _sh in enumerate(S_harm, 1):
    # plt.subplot(3, 2, i)
    # librosa.display.specshow(librosa.amplitude_to_db(_sh,
                                                    #  ref=S.max()),
                            #  sr=sr, y_axis='log')
    # plt.title('h={:.3g}'.format(h_range[i-1]))
    # plt.yticks([])
# plt.tight_layout()
# plt.show()
