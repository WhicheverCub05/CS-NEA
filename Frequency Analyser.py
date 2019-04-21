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


# default_frequency_list = [500, 1000]
default_frequency_list = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]

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
        root.geometry("720x325")
        root.minsize(550, 300)
        root.maxsize(800, 400)
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
        self.setuplabel.pack()

        self.setuptext = Label(self.setupframe, text='            Step 1                '
                                                     '                             Step 2'
                                                     '                                           '
                                                     '  Step 3             ', font='helvetica 11 bold')
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

        self.frequencyinput = Entry(self.inputframe_left, textvariable=user_input_list, width=41)
        self.frequencyinput.pack(side=BOTTOM)

        self.frequencyinput_text = Label(self.inputframe_left, text='Default frequency list = \n 31, 62, 125, 250, '
                                                                    '500, 1000,\n 2000, 4000, 8000, 16000\n\n'
                                                                    'Input custom list - comma separated (,_) \n',
                                         height=6, width=35, bg='#CEDBFF')
        self.frequencyinput_text.pack(side=TOP)

        self.frequencyinput.bind("<Enter>", self.input_box_on_hover)
        self.frequencyinput.bind("<Leave>", self.input_box_off_hover)

        self.startButton = Button(self.startframe, text='Start', font='Helvetica 9 bold', width=10, height=2, bg='#83A4FF')
        self.startButton.bind('<Button-1>', self.start_button)
        self.startButton.pack(side=LEFT)

        self.logtext_title = Label(self.logframe, text='Log: ')
        self.logtext_title.pack(side=TOP)

        self.scrollbar = Scrollbar(self.logframe)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.logtextbox = Text(self.logframe, width=50, height=9, yscrollcommand=self.scrollbar.set)
        self.logtextbox.pack(side=LEFT)
        self.logtextbox.bind("<Key>", lambda e: "break")
        self.logtextbox.config(yscrollcommand=self.scrollbar.set)
        self.logtextbox.see('end')

        self.scrollbar.config(command=self.logtextbox.yview)

        def print_to_gui(printed_statements):
            self.logtextbox.insert(INSERT, printed_statements)
            self.logtextbox.see('end')

        sys.stdout.write = print_to_gui

    def input_box_on_hover(self, event):
        self.frequencyinput_text.configure(text='Frequency Categories\nBass (Boom)       : 60 to 250 hz\nLower Mid '
                                                
                                                '(Kick presence)  : 250 to 500 hz\nHigher Mid (Vocal range)    : '
                                                '500 to 3000 hz\nPresence to treble (Hi hats) : 3000 to 20khz\n'
                                                'Example List : 80, 200, 1000, 16000')

    def input_box_off_hover(self, event):
        self.frequencyinput_text.configure(text='Default frequency list = \n 31, 62, 125, 250, 500, 1000,\n 2000, 4000,'
                                                ' 8000, 16000\nInput custom list - comma separated (,_) ')

    def start_button(self, root):
        if re.search('[a-zA-Z]', StringVar.get(user_input_list)) and frequency_checkbox_state.get() == 1:
            print('---------------------------')
            print("Only use numbers, spaces and commas in list")
            print('---------------------------')
        else:
            print("Starting")
            Mainclass.start_analysing(root)


class Mainclass:

    def __init__(self):
        pass

    def make_user_frequency_list(self):
        user_frequency_list = StringVar.get(user_input_list)
        user_frequency_list = user_frequency_list.split(',')
        correct_user_list = True

        for i in range(len(user_frequency_list)):
            try:
                user_frequency_list[i] = int(user_frequency_list[i])
            except ValueError:
                print("Make sure you input a list of frequencies if the checkbox is ticked")
                correct_user_list = False

        if correct_user_list:  # == True
            return user_frequency_list
        else:
            user_frequency_list = [0]
            return user_frequency_list

    def determine_frequency_list(self):
        if frequency_checkbox_state.get() == 0:
            frequency_list = default_frequency_list
            print('Running with the default frequency list\n')

        else:
            frequency_list = Mainclass().make_user_frequency_list()
            print('Running with the custom frequency list\n')

        return frequency_list

    def produce_sinewave(self, frequency):
        produced_sinewave = [np.sin(2 * np.pi * frequency * x / sample_rate) for x in range(sample_rate)]
        return produced_sinewave

    def append_frequency_list_name(self, frequency):
        file.append("".join(['sinewave_at_', str(frequency), 'hz.wav']))
        return file

    def play_audio_and_record_microphone(self, input_audio, frequency):
        print("playing frequency at ", frequency, "hz")
        recorded_audio = sd.playrec(input_audio, sample_rate, channels=1, dtype='int32')
        sd.wait()
        return recorded_audio

    def write_audio_data(self, recorded_audio, i):
        wav.write(file[i], sample_rate, recorded_audio)

    def read_audio_data(self):
        opened_recording = wave.open(file[i], 'r')
        audio_data_frames = opened_recording.readframes(num_samples)
        opened_recording.close()
        return audio_data_frames

    def process_input_audio(self, audio_data):
        audio_data = struct.unpack('{n}h'.format(n=num), audio_data)
        audio_data = np.array(audio_data)  # [] number can be inserted for a set of frames
        audio_data_fft = np.fft.fft(audio_data)
        audio_data_frequencies = np.abs(audio_data_fft)
        audio_data_rft = np.fft.rfft(audio_data_frequencies/1000000)
        # rft[:15000] = 0 # cuts out everything after 20khz
        smoothed_audio_data_frequencies = np.fft.irfft(audio_data_rft)
        return smoothed_audio_data_frequencies

    def plot_fft_graph(self, input_frequency, audio_data):
        plt.xscale('log')
        plt.yscale('log')
        print("The highest recorded frequency is {} Hz\n".format(np.argmax(audio_data[0:30000])))
        min_plot_for_frequency = int((input_frequency - input_frequency / 10))
        max_plot_for_frequency = int((input_frequency + input_frequency / 10))

        plt.plot(audio_data[min_plot_for_frequency:max_plot_for_frequency], label=("{} Hz".format(input_frequency)))

        plt.legend(bbox_to_anchor=(0, 1), loc=2, borderaxespad=0., fontsize='small', ncol=5)
        plt.title("Frequencies found")
        plt.xlabel('Frequencies/Hz')
        plt.ylabel('Amplitude')

    def display_graph(self, frequency_list):
        min_graph_range = (((min(frequency_list) / 10) * 8) / 10)
        max_graph_range = (((max(frequency_list) / 8) * 10) / 10)

        plt.xlim(min_graph_range, max_graph_range)
        plt.ylim(0.1, 10000)
        plt.show()

    def clear_files(self, file_list):
        for i in range(len(file_list)):
            os.remove(file_list[i])  # was just file

    def start_analysing(self):
        frequency_list = Mainclass().determine_frequency_list()
        try:
            for i in range(len(frequency_list)):

                Mainclass().append_frequency_list_name(frequency_list[i])
                produced_sinewave = Mainclass.produce_sinewave(self, frequency=frequency_list[i])
                root.update_idletasks()

                recorded_audio = Mainclass.play_audio_and_record_microphone(self, input_audio=produced_sinewave,
                                                                            frequency=frequency_list[i])
                audio_data_frames = Mainclass.process_input_audio(self, audio_data=recorded_audio)

                Mainclass.plot_fft_graph(self, input_frequency=frequency_list[i], audio_data=audio_data_frames)

        except FileNotFoundError:
            print('Make sure audio files in use are not being deleted\n '
                  'try restarting program with with a functioning input')

        except sd.PortAudioError:
            print('Make sure your microphone is plugged into your device\n '
                  'try restarting the program with a functioning input')

        except ValueError:
            print('Make sure your frequency list only contains a\n number followed by a comma up to the last frequency')

        try:
            Mainclass().clear_files(file_list=file)
        except:
            pass
        print("-----------End------------\n")

        Mainclass.display_graph(self, frequency_list=frequency_list)


if __name__ == "__main__":
    a = UI(root)  # UI(root)
    root.mainloop()
