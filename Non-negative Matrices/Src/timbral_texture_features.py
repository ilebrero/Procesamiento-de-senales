import librosa
import numpy as np

# Valor arbitrario. Tiene que ser chico, se puede probar con otros a ver como da
DELTA_SPECTRUM_DELTA = 0.05

# Valor arbitrario del paper, se pueden probar otros
SPECTRAL_ROLLOFF_THRESHOLD = 0.85

def sign(val):
  if val >= 0:
    return 1
  else:
    return -1

# TODO: Implementacion ad_hoc, ver como se calcula la resolution real
def DFT_resolution(signal, sampling_rate):
  return int(
    np.ceil(
      sampling_rate / len(signal)
    )
  )

def sample_spectrum(frecuency, i, t, delta):
  return np.log(
    frecuency[i, t]
  ) + delta

# drecado, tambien estaba en librosa
def zero_crossing_rate(signal):
  rate = 0

  for i in range(1, len(signal)):
    rate = rate + np.absolute(
      sign( signal[i] ) 
      - 
      sign( signal[i - 1] ) 
    )

  return rate / len(signal - 1)

# TODO: Terminar, como se calcula K? (resolution of the DFT)
def delta_spectrum(signal, sampling_rate, t_frame):
  res = 0
  DFT_res   = DFT_resolution(signal, sampling_rate)
  frecuency = np.abs(librosa.stft(signal))

  for i in range(0, DFT_res):
    res = res + np.square(
      sample_spectrum(frecuency, i, t_frame, DELTA_SPECTRUM_DELTA)
      -
      sample_spectrum(frecuency, i, t_frame-1, DELTA_SPECTRUM_DELTA)
    )
  
  return res / (DFT_res - 1)

# TODO: terminar, como se calcula K? (resolution of the DFT)
def spectral_rolloff(signal, sampling_rate, t_frame):
  res   = 0
  upper_bound = 0
  DFT_res = DFT_resolution(signal, sampling_rate)
  frecuency = np.abs(librosa.stft(signal))

  for i in range(0, DFT_res):
    upper_bound = upper_bound + frecuency[i, t_frame]

  upper_bound = upper_bound * SPECTRAL_ROLLOFF_THRESHOLD

  for i in range(0, DFT_res):
    proximo_val = res + frecuency[i, t_frame]
    
    if proximo_val >= upper_bound:
      return res
    else:
      res = proximo_val

def generate_delta_spectrum_feature_vector(signal, sampling_rate):
  frecuency  = librosa.stft(signal)
  _, columns = frecuency.shape 
  feature_vector = np.array([])

  for i in range(columns):
    feature_vector = np.append(
      feature_vector,
      delta_spectrum(
        signal, 
        sampling_rate,
        i
      )
    )

  return feature_vector

# @deprecated(version='1.2.1', reason="Habia una hecha en librosa")
def generate_spectral_rolloff_feature_vector(signal, sampling_rate):
  frecuency  = librosa.stft(signal)
  _, columns = frecuency.shape 
  feature_vector = np.array([], dtype=float)

  for i in range(columns):
    feature_vector = np.append(
      feature_vector,
      spectral_rolloff(
        signal, 
        sampling_rate, 
        i
      )
    )

  return feature_vector


# Nota: representamos los vectores de features como columnas
def generate_audio_features(signal, sampling_rate):
  # spectral_rolloff = librosa.feature.spectral_rolloff(signal, sampling_rate)
  # spectral_rolloff = np.reshape(
  #   spectral_rolloff,
  #   spectral_rolloff.size, 
  #   order='F'
  # )

  return np.array([
    # Primeros features
    np.array(librosa.feature.zero_crossing_rate(signal)[0]),
    # np.array(generate_delta_spectrum_feature_vector(signal, sampling_rate)),
    np.array(librosa.feature.spectral_rolloff(signal, sampling_rate)[0]),

    # Segundos features
    np.array(librosa.feature.spectral_centroid(y=signal, sr=sampling_rate)[0]),
    np.array(librosa.feature.spectral_flatness(y=signal)[0]),
  ]).T