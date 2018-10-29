import sounddevice as sd
from pylab import *
import struct
import wave
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav

'''
frequency = [20, 30, 40, 60, 80, 120, 160, 200, 240, 300, 360, 420, 480, 720, 960, 1440, 1920, 2400, 2640, 2880, 3360,
3600, 3840, 4000, 4300, 4600, 4845, 5000, 5347, 5500, 5850, 6000, 6300, 6600, 7000, 7680, 8200, 8800, 9300, 9900, 10100,
10600, 11200, 11700, 12200, 13300, 14000, 14400, 15000, 15720]
'''

frequencyList = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
sample_rate = 48000
sd.default.samplerate = sample_rate
sd.default.channels = 1
file = []
num_samples = sample_rate
sampling_rate = sample_rate
num = num_samples*2
i = 0

class MainClass:

    def __init__(self):
        pass

    def frequency_list(self):
        for i in range(len(frequencyList)):
            file.append("".join(['test_', str(frequencyList[i]), 'hz.wav']))
            i = i + 1
        return file

    def sinewave(self):
        sine = [np.sin(2 * np.pi * frequencyList[i] * x / sample_rate) for x in range(sample_rate)]
        return sine

    def play_rec(self, sinewave, i):
        print("playing", frequencyList[i], "hz and recording")
        recording = sd.playrec(MainClass.sinewave(self), sample_rate, channels=1, dtype='int32')
        sd.wait()
        return recording

    def plot_graph(self, play_rec, sinewave):
        for i in range(len(frequencyList)):
            wav.write(file[i], sample_rate, MainClass().play_rec(MainClass.sinewave(self), i))
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

    def clear_files(self, frequency_list):
        for i in range(len(frequency_list)):
            os.remove(file[i])


def default_run():
    for i in range(len(frequencyList)):
        MainClass().frequency_list()
        MainClass().sinewave()
        MainClass().play_rec(MainClass().sinewave(), i)
        # MainClass().plot_graph(MainClass().sinewave(), MainClass().play_rec(MainClass().sinewave(), i))
        i = i+1


default_run()

'''
for i in range(len(frequencyList)):
    os.remove(file[i])
'''


