import sounddevice as sd
from pylab import *
import struct
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import re


default_frequency_list = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]

sample_rate = 48000
sd.default.channels = 1
sd.default.samplerate = sample_rate
num_samples = sample_rate
sampling_rate = sample_rate
root = Tk()
frequency_checkbox_state = IntVar()
user_input_list = StringVar()


class UI:

    def __init__(self, master):
        root.geometry("720x325")
        root.minsize(550, 300)
        root.maxsize(800, 400)
        # root.iconbitmap('icon1.ico'), to used when icon and program are locally stored
        root.title('Frequency Analyser')

        self.main_frame = Frame(root)
        self.main_frame.pack()

        self.graph_frame = Frame(root)
        self.graph_frame.pack(side=BOTTOM)

        self.top_frame = Frame(self.main_frame)
        self.top_frame.pack(side=TOP)

        self.setup_frame = Frame(self.top_frame, border=5)
        self.setup_frame.pack(side=TOP)

        self.mid_frame = Frame(self.main_frame, border=5)
        self.mid_frame.pack(side=TOP)

        self.start_frame = Frame(self.mid_frame, border=5)
        self.start_frame.pack(side=LEFT)

        self.input_frame = Frame(self.start_frame)
        self.input_frame.pack(side=BOTTOM)

        self.input_frame_left = Frame(self.input_frame)
        self.input_frame_left.pack(side=LEFT)

        self.bottom_frame = Frame(self.main_frame)
        self.bottom_frame.pack(side=BOTTOM, )

        self.log_frame = Frame(self.mid_frame, border=5)
        self.log_frame.pack(side=RIGHT)

        self.setup_label = Label(self.setup_frame, text='Setup before running the program', height=2)
        self.setup_label.pack()

        self.setup_text = Label(self.setup_frame, text='            Step 1                '
                                                       '                             Step 2'
                                                       '                                           '
                                                       '  Step 3             ', font='helvetica 11 bold')
        self.setup_text.pack()

        self.step_text1 = Label(self.setup_frame, text='make sure your \n microphone \n is connected', width=20)
        self.step_text1.pack(side=LEFT)

        self.step_text3 = Label(self.setup_frame, text='make sure to have \n your microphone \n in its used position',
                                width=20)
        self.step_text3.pack(side=RIGHT)

        self.step_text2 = Label(self.setup_frame, text='make sure the volume\n on the microphone and speaker are\n'
                                                       'at the level of intended use', width=30)
        self.step_text2.pack()

        self.Checkbox = Checkbutton(self.start_frame, state=ACTIVE, variable=frequency_checkbox_state,
                                    text='Run custom \n frequencies?', height=3, width=14)
        self.Checkbox.pack(side=LEFT)

        self.user_frequency_input = Entry(self.input_frame_left, textvariable=user_input_list, width=41)
        self.user_frequency_input.pack(side=BOTTOM)

        self.frequencyinput_text = Label(self.input_frame_left, text='Default frequency list = \n 31, 62, 125, 250, '
                                                                     '500, 1000,\n 2000, 4000, 8000, 16000\n\n'
                                                                     'Input custom list - comma separated (,_) \n',
                                         height=6, width=35, bg='#CEDBFF')
        self.frequencyinput_text.pack(side=TOP)

        self.user_frequency_input.bind("<Enter>", self.input_box_on_hover)
        self.user_frequency_input.bind("<Leave>", self.input_box_off_hover)

        self.start_Button = Button(self.start_frame, text='Start', font='Helvetica 9 bold', width=10, height=2,
                                   bg='#83A4FF')
        self.start_Button.bind('<Button-1>', self.start_button)
        self.start_Button.pack(side=LEFT)

        self.logtext_title = Label(self.log_frame, text='Log: ')
        self.logtext_title.pack(side=TOP)

        self.scrollbar = Scrollbar(self.log_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.logtext_box = Text(self.log_frame, width=52, height=9, yscrollcommand=self.scrollbar.set)
        self.logtext_box.pack(side=LEFT)
        self.logtext_box.bind("<Key>", lambda e: "break")
        self.logtext_box.config(yscrollcommand=self.scrollbar.set)
        self.logtext_box.see('end')

        self.scrollbar.config(command=self.logtext_box.yview)

        def print_to_gui(printed_statements):
            self.logtext_box.insert(INSERT, printed_statements)
            self.logtext_box.see('end')

        sys.stdout.write = print_to_gui

    def input_box_on_hover(self, event):
        self.frequencyinput_text.configure(text='Frequency Categories\nBass (Boom)       : 60 to 250 hz\nLower Mid '
                                                '(Kick presence)  : 250 to 500 hz\nHigher Mid (Vocal range)    : '
                                                '500 to 3000 hz\nPresence to treble (Hi hats) : 3000 to 20khz\n'
                                                'Example List : 80, 200, 1000, 16000')

    def input_box_off_hover(self, event):
        self.frequencyinput_text.configure(text='Default frequency list = \n 31, 62, 125, 250, 500, 1000,\n 2000, 4000,'
                                                ' 8000, 16000\nInput custom list - comma separated (,_) ')

    def check_validity_of_user_frequency_list(self):
        list_is_valid = False
        if re.search('[a-zA-Z]', StringVar.get(user_input_list)) and frequency_checkbox_state.get() == 1:
            print('---------------------------')
            print("Only use numbers, spaces and commas in your list")
            print('---------------------------')

        elif not StringVar.get(user_input_list).strip()and frequency_checkbox_state.get() == 1:
            print('---------------------------')
            print("Make sure to input a list if the checkbox is ticked")
            print('---------------------------')

        else:
            list_is_valid = True

        return list_is_valid

    def start_button(self, root):
            if self.check_validity_of_user_frequency_list():
                print("Starting")
                Mainclass().start_analysing()

            else:
                pass


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
                print('---------------------------')
                print("Only use numbers, spaces and commas in your list")
                print('---------------------------')
                correct_user_list = False
        if correct_user_list:  # == True
            return user_frequency_list
        else:
            user_frequency_list = [1]
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

    def play_audio_and_record_microphone(self, input_audio, frequency):
        print("playing frequency at ", frequency, "hz")
        recorded_audio = sd.playrec(input_audio, sample_rate, channels=1, dtype='int32')
        sd.wait()

        return recorded_audio

    def process_input_audio(self, audio_data):
        audio_data = struct.unpack('{n}h'.format(n=num_samples*2), audio_data)
        audio_data = np.array(audio_data)  # [] number can be inserted for a set of frames
        audio_data_fft = np.fft.fft(audio_data)
        audio_data_absolute = np.abs(audio_data_fft)
        audio_data_rfft = np.fft.rfft(audio_data_absolute)/1000000
        smoothed_audio_data = np.fft.irfft(audio_data_rfft)

        return smoothed_audio_data

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
        plt.ylim(0.1, 100000)
        plt.show()

    def start_analysing(self):
        frequency_list = Mainclass().determine_frequency_list()
        try:
            for i in range(len(frequency_list)):
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

        print("-----------End------------\n")

        Mainclass.display_graph(self, frequency_list=frequency_list)


if __name__ == "__main__":
    a = UI(root)  # UI(root)
    root.mainloop()
