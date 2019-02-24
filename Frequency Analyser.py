import sounddevice as sd
from pylab import *
import struct
import wave
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from tkinter import *
import re


default_frequency_list = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
# default_frequency_list = [1000, 200, 400]  for testing
file = []
i = 0
sample_rate = 48000
sd.default.samplerate = sample_rate
sd.default.channels = 1
num_samples = sample_rate
sampling_rate = sample_rate
num = num_samples * 2
root = Tk()
frequency_checkbox_state = IntVar()
user_input_list = StringVar()


class UI:

    def __init__(self, master):
        root.geometry("720x300")
        root.minsize(500, 275)
        # root.iconbitmap('icon1.ico')
        root.title('Frequency Analyser')

        self.mainframe = Frame(root)
        self.mainframe.pack()

        self.graphframe = Frame(root)
        self.graphframe.pack(side=BOTTOM)

        self.topframe = Frame(self.mainframe)
        self.topframe.pack(side=TOP)

        self.setupframe = Frame(self.topframe, border=5)
        self.setupframe.pack(side=TOP)

        self.midframe = Frame(self.mainframe, border=5)
        self.midframe.pack(side=TOP)

        self.startframe = Frame(self.midframe, border=5)
        self.startframe.pack(side=LEFT)

        self.inputframe = Frame(self.startframe)
        self.inputframe.pack(side=BOTTOM)

        self.inputframe_left = Frame(self.inputframe)
        self.inputframe_left.pack(side=LEFT)

        self.bottomframe = Frame(self.mainframe)
        self.bottomframe.pack(side=BOTTOM, )

        self.logframe = Frame(self.midframe, border=5)
        self.logframe.pack(side=RIGHT)

        self.setuplabel = Label(self.setupframe, text='Setup before running the program', height=2)
        self.setuplabel.pack(side=TOP)

        self.setuptext = Label(self.setupframe, text='                 Step 1                          '
                                                     '                      Step 2'
                                                     '                                           '
                                                     '           Step 3                  ')
        self.setuptext.pack()

        self.steptext1 = Label(self.setupframe, text='make sure your \n microphone \n is connected', width=20)
        self.steptext1.pack(side=LEFT)

        self.steptext3 = Label(self.setupframe, text='make sure to have \n your microphone \n in its used position',
                               width=20)
        self.steptext3.pack(side=RIGHT)

        self.steptext2 = Label(self.setupframe, text='make sure the volume\n on the microphone and speaker are\n'
                                                     'at the level of intended use', width=30)
        self.steptext2.pack()

        self.Checkbox = Checkbutton(self.startframe, state=ACTIVE, variable=frequency_checkbox_state,
                                    text='Run custom \n frequencies?', height=3, width=14)
        self.Checkbox.pack(side=LEFT)

        self.frequencyinput = Entry(self.inputframe_left, textvariable=user_input_list, width=37)
        self.frequencyinput.pack(side=BOTTOM)

        self.frequencyinput_text = Label(self.inputframe_left, text='Default frequency list = \n 31, 62, 125, 250, '
                                                                    '500, 1000,\n 2000, 4000, 8000, 16000\n\n'
                                                                    'Input custom list - comma separated (,_) ',
                                         height=5, bg='#CEDBFF')
        self.frequencyinput_text.pack(side=TOP)

        self.startButton = Button(self.startframe, text='Start', font='Helvetica 9 bold', width=10, height=2, bg='#83A4FF')
        self.startButton.bind('<Button-1>', self.start_button)
        self.startButton.pack(side=LEFT)

        self.logtext_title = Label(self.logframe, text='Log: ')
        self.logtext_title.pack(side=TOP)

        self.scrollbar = Scrollbar(self.logframe)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.logtextbox = Text(self.logframe, width=55, height=7, yscrollcommand=self.scrollbar.set)
        self.logtextbox.pack(side=LEFT)
        self.logtextbox.bind("<Key>", lambda e:"break")

        self.scrollbar.config(command=self.logtextbox.yview)

        def print_to_gui(printed_statements):
            self.logtextbox.insert(INSERT, printed_statements)

        sys.stdout.write = print_to_gui

    def start_button(self, root):
        if re.search('[a-zA-Z]', StringVar.get(user_input_list)) and frequency_checkbox_state.get() == 1:
            print('---------------------------')
            print("Only use numbers, spaces and commas in list")
            print('---------------------------')
        else:
            print("Starting")
            Mainclass.start(root)
            print("End")


class Mainclass:

    def __init__(self):
        pass

    def make_user_frequency_list(self):
        user_frequency_list = StringVar.get(user_input_list)
        user_frequency_list = user_frequency_list.split(',')

        for i in range(len(user_frequency_list)):
            user_frequency_list[i] = int(user_frequency_list[i])

        return user_frequency_list

    def determine_frequency_list(self):
        if frequency_checkbox_state.get() == 0:
            frequency_list = default_frequency_list
            print('checkbox is off')

        else:

            frequency_list = Mainclass().make_user_frequency_list()
            print("checkbox is on")

        return frequency_list

    def sinewave(self, frequency):
        sine = [np.sin(2 * np.pi * frequency * x / sample_rate) for x in range(sample_rate)]
        return sine

    def frequency_list_name(self, frequency):
        file.append("".join(['sinewave_at_', str(frequency), 'hz.wav']))
        return file

    def play_rec(self, sinewave, frequency):
        print("playing frequency at ", frequency, "hz")
        recording = sd.playrec(sinewave, sample_rate, channels=1, dtype='int32')
        sd.wait()
        return recording

    def plot_graph(self, recording, i):
        wav.write(file[i], sample_rate, recording)
        rec = wave.open(file[i], 'r')
        data = rec.readframes(num_samples)
        rec.close()
        data = struct.unpack('{n}h'.format(n=num), data)
        data = np.array(data)  # [] number can be inserted for a set of frames
        data_fft = np.fft.fft(data)
        frequencies = np.abs(data_fft)
        plt.xscale('log')
        plt.yscale('log')
        print("The highest recorded frequency is {} Hz".format(np.argmax(frequencies[0:20000])))
        plt.plot(frequencies[0:20000])
        plt.title("Frequencies found")
        plt.xlim(27, 20000)
        plt.ylim(100000, 1000000000)
        plt.savefig('wave{}.png'.format(i))

    def clear_files(self, file):
        for i in range(len(file)):
            os.remove(file[i])

    def start(self):
        frequency_list = Mainclass().determine_frequency_list()
        try:
            for i in range(len(frequency_list)):
                Mainclass().frequency_list_name(frequency_list[i])
                Mainclass().plot_graph(recording=Mainclass().play_rec(sinewave=Mainclass().sinewave(frequency=frequency_list[i]), frequency=frequency_list[i]), i=i)

        except FileNotFoundError:
            print('Make sure audio files in use are not being deleted\n '
                  'try restarting program with with a functioning input')

        except sd.PortAudioError:
            print('Make sure your microphone is plugged into your device\n '
                  'try restarting the program with a functioning input')

        Mainclass().clear_files(file=file)
        print('')

        plt.show()


if __name__ == "__main__":
    a = UI(root)
    root.mainloop()
