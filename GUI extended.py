from tkinter import *

root = Tk()

class TheClass:

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


b = TheClass(root)
root.mainloop()  # to keep window open
