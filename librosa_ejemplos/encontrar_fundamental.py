from scipy import signal as sg
import librosa
import numpy as np


#function to find the fundamental pitch frequency counting zeroes
#From https://www.kaggle.com/asparago/simple-pitch-detector
def find_fundamental(signal, sampling_ratio):
  signal = signal
  #one should be careful in deciding if it is worth analysing the entire record or
  #just chunks of it, and excluding more noisy parts  
  #signal=signal[:len(signal)/2]
  rate = sampling_ratio #wf.getframerate()
  swidth = len(signal) # wf.getsampwidth()
  #first of all we remove the horizontal offset
  signal = signal - np.mean(signal)
  #now we calculate the autocorrelation of the signal against itself but inverted in time
  #and we throw away negative lags
  corr = sg.fftconvolve(signal, signal[::-1], mode='full')
  corr = corr[int(len(corr)/2):]
  diff = np.diff(corr)
  n = [i for i in range(0,len(diff)) if diff[i]>0][0]
  peak = np.argmax(corr[n:]) + n
  return rate/peak


y, sr = librosa.load("../audios/test.wav")
a = find_fundamental(y, sr)
print(a)
# A3 -> 11.516698
# A4 -> 1464
# A3 -> 1193
# A3 forte -> 504