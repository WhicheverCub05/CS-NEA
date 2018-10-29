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

'''
frequency = [20, 30, 40, 60, 80, 120, 160, 200, 240, 300, 360, 420, 480, 720, 960, 1440, 1920, 2400, 2640, 2880, 3360,
3600, 3840, 4000, 4300, 4600, 4845, 5000, 5347, 5500, 5850, 6000, 6300, 6600, 7000, 7680, 8200, 8800, 9300, 9900, 10100,
10600, 11200, 11700, 12200, 13300, 14000, 14400, 15000, 15720]
'''
frequency = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
sample_rate = 48000
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


def play_rec(sine, i):
    print("playing", frequency[i], "hz and recording")
    recording = sd.playrec(sinewave(), sample_rate, channels=1, dtype='int32')
    sd.wait()
    return recording


for i in range(len(frequency)):
    wav.write(file[i], sample_rate, play_rec(sinewave(), i))
    rec = wave.open(file[i], 'r')
    data = rec.readframes(num_samples)  # was num_samples
    rec.close()
    data = struct.unpack('{n}h'.format(n=num), data)
    data = np.array(data)  # [] number can be inserted for a set of frames
    data_fft = np.fft.fft(data)
    frequencies = np.abs(data_fft)
    plt.xscale('log')
    plt.yscale('log')
    print("The highest frequency is {} Hz".format(np.argmax(frequencies[0:20000])))
    plt.plot(frequencies[0:20000])
    plt.title("Frequencies found")
    plt.xlim(27, 20000)  # (0, 20000)
    plt.ylim(100000, 1000000000)
    plt.savefig('wave.png')
    i = i+1


plt.show()

for i in range(len(frequency)):
    os.remove(file[i])

