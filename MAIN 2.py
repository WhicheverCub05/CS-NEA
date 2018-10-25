import sounddevice as sd
import scipy.io.wavfile as wav
from pylab import *
import struct
import wave
import os
from pydub import AudioSegment as ag
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import pylab


frequency = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
sample_rate = 96000
sd.default.samplerate = sample_rate
sd.default.channels = 1
file = []
num_samples = sample_rate
sampling_rate = sample_rate
num = num_samples*2
i = 0


for i in range(len(frequency)):
    file.append("".join(['test_', str(frequency[i]), 'hz.wav']))
    i = i + 1


def sinewave():
    sine = [np.sin(2 * np.pi * frequency[i] * x / sample_rate) for x in range(sample_rate)]
    return sine


def play_rec(sine):
    print("playing", frequency[i], "hz and recording")
    recording = sd.playrec(sinewave(), sample_rate, channels=1, dtype='int32')
    sd.wait()
    return recording


for i in range(len(frequency)):
    wav.write(file[i], sample_rate, play_rec(sinewave()))
    rec = wave.open(file[i], 'r')
    data = rec.readframes(num_samples)
    rec.close()
    data = struct.unpack('{n}h'.format(n=num), data)
    data = np.array(data)
    data_fft = np.fft.fft(data)
    frequencies = np.abs(data_fft)
    plt.xscale('log')
    print("The highest frequency is {} Hz".format(np.argmax(frequencies[0:20000])))
    plt.plot(frequencies[27:20000])
    plt.title("Frequencies found")
    plt.xlim(27, 20000)  # (0, 20000)
    plt.savefig('wave.png')
    i = i+1


plt.show()

for i in range(len(frequency)):
    os.remove(file[i])

