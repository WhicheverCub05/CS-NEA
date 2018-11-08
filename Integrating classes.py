import sounddevice as sd
from pylab import *
import struct
import wave
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from tkinter import *

default_frequency_list = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
file = []

sample_rate = 48000
sd.default.samplerate = sample_rate
sd.default.channels = 1
num_samples = sample_rate
sampling_rate = sample_rate
num = num_samples*2
root = Tk()


class UI:

    def __init__(self, master):

        root.geometry("575x725")
        root.iconbitmap('icon1.ico')
        root.title('Frequency Analyser')

        self.topframe = Frame(root)
        self.topframe.pack(side=TOP)

        self.setupframe = Frame(self.topframe)
        self.setupframe.pack(side=TOP)

        self.midframe = Frame(root)
        self.midframe.pack(side=TOP)

        self.inputframe = Frame(self.midframe)
        self.inputframe.pack(side=BOTTOM)

        self.bottomframe = Frame(root)
        self.bottomframe.pack(side=BOTTOM,)

        self.logframe = Frame(self.bottomframe)
        self.logframe.pack(side=TOP)

        self.setuplabel = Label(self.setupframe, text='Setup before running the program', height=2)
        self.setuplabel.pack(side=TOP)

        self.setuptext = Label(self.setupframe, text='            Step 1                               '
                                                     '                      Step 2'
                                                     '                                           '
                                                     '           Step 3          ')
        self.setuptext.pack()

        self.steptext1 = Label(self.setupframe, text='make sure the inline \n is outputting')
        self.steptext1.pack(side=LEFT)

        self.steptext3 = Label(self.setupframe, text='Run the sequence')
        self.steptext3.pack(side=RIGHT)

        self.steptext2 = Label(self.setupframe, text='make sure the volume\n on the inline and output are\n'
                                                     'at the level of intended use')
        self.steptext2.pack()

        self.printCheckbox = Checkbutton(self.midframe, text='Run custom frequencies?', height=3)
        self.printCheckbox.pack(side=RIGHT)

        self.startButton = Button(self.midframe, text='Start', width=10, height=2, bg='#00B7FF')
        self.startButton.pack(side=LEFT)

        self.frequencydata = Entry(self.inputframe, width=30)
        self.frequencydata.pack(side=RIGHT)

        self.frequencytext = Label(self.inputframe, text='Input List - comma separated (,_):', height=2)
        self.frequencytext.pack(side=LEFT)

        self.logtext = Label(self.logframe, text='Log: ')
        self.logtext.pack(side=LEFT)

        self.logtextbox = Text(self.logframe, width=41, height=2)
        self.logtextbox.pack(side=RIGHT)

        self.graphtext = Label(self.bottomframe, text='Graph')  # closes the mainloop()
        self.graphtext.pack(side=TOP)

        self.photo = PhotoImage(file='wave.png')
        self.graph = Label(self.bottomframe, image=self.photo)
        self.graph.pack(side=BOTTOM)


b = UI(root)
root.mainloop()  # to keep window open


class Mainclass:

    def __init__(self):
        pass

    def make_frequency_list(self, user_frequency_list):
        while UI.printCheckbox == TRUE:
            frequency_list = default_frequency_list

        else:
            if user_frequency_list[0:len(user_frequency_list)] != int_:
                print('incorrect frequency list')  # to be run to log box

            else:
                frequency_list = user_frequency_list

        return frequency_list

    def sinewave(self, frequency):
        sine = [np.sin(2 * np.pi * frequency * x / sample_rate) for x in range(sample_rate)]
        return sine

    def frequency_list_name(self, frequency_list):
        for i in range(len(frequency_list)):
            file.append("".join(['test_', str(frequency_list[i]), 'hz.wav']))
        return file

    def play_rec(self, sinewave, frequency):
        print("playing", frequency, "hz and recording")
        recording = sd.playrec(sinewave, sample_rate, channels=1, dtype='int32')
        sd.wait()
        return recording

    def plot_graph(self, recording):
        wav.write(file, sample_rate, recording)
        rec = wave.open(file, 'r')
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

    def clear_files(self, frequency_list):
        for i in range(len(frequency_list)):
            os.remove(file[i])
        os.remove('wave.png')




