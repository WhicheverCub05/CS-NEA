import sounddevice as sd
from pylab import *
import struct
import wave
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from tkinter import *


# default_frequency_list = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
default_frequency_list = [1000, 200, 400]  # for testing
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
        root.geometry("575x275")
        # root.iconbitmap('icon1.ico')
        # root.title('Frequency Analyser')

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

        self.Checkbox = Checkbutton(self.startframe, state=ACTIVE, variable=frequency_checkbox_state,
                                    text='Run custom \n frequencies?', height=3)
        self.Checkbox.pack(side=LEFT)


        self.frequencyinput = Entry(self.inputframe_left, textvariable=user_input_list, width=37)
        self.frequencyinput.pack(side=BOTTOM)

        self.frequencytext = Label(self.inputframe_left, text='Input List - comma separated (,_)', height=2)
        self.frequencytext.pack(side=TOP)

        self.logtext = Label(self.logframe, text='Log: ')
        self.logtext.pack(side=TOP)

        self.logtextbox = Text(self.logframe, width=30, height=5)
        self.logtextbox.pack(side=RIGHT)

        #self.graphtext = Label(self.bottomframe, text='')  #
        #self.graphtext.pack(side=TOP)

        self.startButton = Button(self.startframe, text='Start', width=10, height=2, bg='#00B7FF')
        self.startButton.bind('<Button-1>', self.start_button)
        self.startButton.pack(side=LEFT)

        #self.graphtext = Label(self.bottomframe, text='Graph')

        self.photo = PhotoImage(file='wave.png')
        self.graph = Label(self.bottomframe, image=self.photo)

        self.scrollbar = Scrollbar(self.bottomframe)
        self.scrollbar.pack(side=RIGHT, fill=Y)

    #    def clear_image(self):
    #       self.photo = Label(self.bottomframe, image='')

        self.graphtext = Label(self.graphframe, text='Graph')

        self.graph = Label(self.bottomframe, image=self.photo)


    def display_graph(self):
        self.mainframe.pack_forget()
        root.geometry("575x775")
        self.graphtext.pack(side=TOP)
        self.photo = PhotoImage(file='wave0.png')
        self.graph.pack(side=BOTTOM)

    def start_button(self, root):
        print("attempting to start")
        # self.make_user_frequency_list()
        # print('made the frequency list')
        Mainclass.start(root)
        # self.display_graph()
        print("it went through")


class Mainclass:

    def __init__(self):
        pass

    def make_user_frequency_list(self):
        print('make user f list input:', StringVar.get(user_input_list))
        # self.user_frequency_list = '[' + StringVar.get(self.user_input_list) + ']'
        # print('self.user_frequency_list b4 exec: ', self.user_frequency_list)
        user_frequency_list = StringVar.get(user_input_list)
        user_frequency_list = user_frequency_list.split(',')
        # exec(self.user_frequency_list)
        print("self.user frequency_list = ", user_frequency_list)

        for i in range(len(user_frequency_list)):
            user_frequency_list[i] = int(user_frequency_list[i])
            print('self.user_frequency_list in make: ', user_frequency_list)

        return user_frequency_list

    def determine_frequency_list(self):

        # frequency_list = UI(root).make_user_frequency_list.__get__(object)
        # print('frequency list at determine frequency list : ', )
        # print("checkbox is on")

        if frequency_checkbox_state.get() == 0:  # if UI(root).self.printCheckbox == FALSE:
            frequency_list = default_frequency_list
            print('checkbox is off')

        else:

            frequency_list = Mainclass().make_user_frequency_list()
            # frequency_list = UI.make_user_frequency_list.__get__(object, list)
            print("checkbox is on")
            print('frequency_list in dfl is ', frequency_list)
        """
            for i in range in len(frequency_list):
                frequency_list[i].int
        """
        return frequency_list

    def sinewave(self, frequency):
        sine = [np.sin(2 * np.pi * frequency * x / sample_rate) for x in range(sample_rate)]
        return sine

    def frequency_list_name(self, frequency):
        file.append("".join(['sinewave_at_', str(frequency), 'hz.wav']))
        return file

    def play_rec(self, sinewave, frequency):
        print("playing", frequency, "hz and recording")
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
        print("The highest frequency is {} Hz".format(np.argmax(frequencies[0:20000])))
        plt.plot(frequencies[0:20000])
        plt.title("Frequencies found")
        plt.xlim(27, 20000)
        plt.ylim(100000, 1000000000)
        plt.savefig('wave{}.png'.format(i))


        #plt.savefig('wave.png') #  plt.savefig('wave{}.png'.format(i))


    def clear_files(self, file):
        for i in range(len(file)):
            os.remove(file[i])

    # frequency list replaced default frequency list on every single occurrence

    def start(self):
        frequency_list = Mainclass().determine_frequency_list()
        # Mainclass().frequency_list_name(frequency_list=Mainclass().make_frequency_list())
        # print(Mainclass.make_frequency_list.frequency_list)
        # for i in range(len(frequency_list)):
        i = 0
        print("frequency_list (i) in Mainclass().start: ", frequency_list[i])
        sd.wait()
        print('i in start(): ', i)
        print('fl in mainclass().start: ', frequency_list)

        for i in range(len(frequency_list)):
            Mainclass().frequency_list_name(frequency_list[i])
            Mainclass().plot_graph(recording=Mainclass().play_rec(sinewave=Mainclass().sinewave(frequency=frequency_list[i]), frequency=frequency_list[i]), i = 0)

        plt.show()
        print('_________________________________')
        sd.wait()



'''
# potentually can be deleted

    def show_graph(self, i): # was in Mainclass
        Mainclass().plot_graph(recording=Mainclass().play_rec(sinewave=Mainclass().sinewave(frequency=default_frequency_list[i]), frequency=default_frequency_list[i]), i=i)
        print('show_graph i: ', i)
'''

if __name__ == "__main__":
    a = UI(root)  # .Appearance()
    root.mainloop()

# try to make the frequency list work out in the start, make_user_frequency_list
